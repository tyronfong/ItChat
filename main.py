import thread
import re, time
import itchat
import sys
from itchat.content import *

reload(sys)
sys.setdefaultencoding('utf8')

friend_msgs = {}
group_msgs = {}


def enqueue_friend_msg(msg):
    insert_flag = False
    for user in friend_msgs:
        if user == msg['User']['UserName']:
            friend_msgs[user]['msgs'] += [msg]
            friend_msgs[user]['unreadAmount'] += 1
            insert_flag = True
            break
    if not insert_flag:
        # it is a new msg which was not enqueue before
        friend_msgs[msg['User']['UserName']] = {'displayName': msg['User']['RemarkName'] if msg['User']['RemarkName'] != '' else msg['User']['NickName'], 'msgs': [msg], 'unreadAmount': 1}


def enqueue_group_msg(msg):
    insert_flag = False
    for group in group_msgs:
        if group == msg['User']['UserName']:
            group_msgs[group]['msgs'] += [msg]
            group_msgs[group]['unreadAmount'] += 1
            insert_flag = True
            break
    if not insert_flag:
        # it is a new msg which was not enqueue before
        group_msgs[msg['User']['UserName']] = {'displayName': msg['User']['NickName'], 'msgs': [msg], 'unreadAmount': 1}


def print_friend_msgs(show_history=False):
    print('====Friend Messages==============')
    for user_name in friend_msgs:
        print('%s-----(%s):' % (friend_msgs[user_name]['displayName'], find_friend_index_by_name(user_name)))
        start_position = 0 if show_history else (len(friend_msgs[user_name]['msgs']) - friend_msgs[user_name]['unreadAmount'])
        for i, val in enumerate(friend_msgs[user_name]['msgs'][start_position:]):
            if val['User']['UserName'] == val['FromUserName']:
                print('%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(val['CreateTime'])), my_align(friend_msgs[user_name]['displayName'], 16), val['Text']))
            else:
                print('%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(val['CreateTime'])), my_align(u'\u6211', 16), val['Text']))
        friend_msgs[user_name]['unreadAmount'] = 0
        # print line
        print


def print_group_msgs(show_history=False):
    print('====Group Messages===============')
    for group_name in group_msgs:
        print('%s-----(%s):' % (group_msgs[group_name]['displayName'], find_group_index_by_name(group_name)))
        start_position = 0 if show_history else (len(group_msgs[group_name]['msgs']) - group_msgs[group_name]['unreadAmount'])
        for i, val in enumerate(group_msgs[group_name]['msgs'][start_position:]):
            if val['User']['UserName'] == val['FromUserName']:
                print('%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(val['CreateTime'])), my_align(val['ActualNickName'], 16), val['Text']))
            else:
                print('%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(val['CreateTime'])), my_align(u'\u6211', 16), val['Text']))
        group_msgs[group_name]['unreadAmount'] = 0
        # print line
        print


def find_friend_index_by_name(user_name):
    for i, val in enumerate(itchat.originInstance.memberList):
        if user_name == val['UserName']:
            return i


def find_friend_name_by_index(user_index):
    return itchat.originInstance.memberList[user_index]['UserName']


def find_group_index_by_name(group_name):
    for i, val in enumerate(itchat.originInstance.chatroomList):
        if group_name == val['UserName']:
            return i


def find_group_name_by_index(group_index):
    return itchat.originInstance.chatroomList[group_index]['UserName']


def print_msgs(show_history=False):
    print_friend_msgs(show_history)
    print_group_msgs(show_history)


def find_chinese(text):
    if not isinstance(text, unicode):
        text = text.decode('utf8')
    res = re.findall(u"[\u4e00-\u9fa5]", text)
    return res


def my_align(un_align_str, length=0, addin=' '):
    assert isinstance(length, int)
    if length <= len(un_align_str):
        return un_align_str
    strlen = len(un_align_str)
    chn = find_chinese(un_align_str)
    numchn = len(chn)
    numsp = length - strlen - numchn
    str = addin * numsp
    return un_align_str + str


@itchat.msg_register(TEXT, isGroupChat=True)
def receive_group_msg(msg):
    enqueue_group_msg(msg)
    print(msg)
    print('received group msg.')


@itchat.msg_register(TEXT, isFriendChat=True)
def receive_friend_msg(msg):
    enqueue_friend_msg(msg)
    print(msg)
    print(msg['Text'])
    print('received friend msg.')


itchat.auto_login(True)
thread.start_new_thread(itchat.run, ())
useage_text = 'Usage:\n' \
              '    p          (pull all unread messages with "member ref" witch is used for reply)\n' \
              '    pa         (pull all cached historic messages with "member ref" witch is used for reply)\n' \
              '    rg [target group ref] [message content]\n' \
              '               (reply message to specific group,\n' \
              '                e.g. reply 0 where are you?)\n' \
              '    r [target user ref] [message content]\n' \
              '               (reply message to specific user,\n' \
              '                e.g. reply 1 where are you?)\n' \
              '    h          (show help menu)'
while 1:
    command = raw_input()
    if command.strip().find('h') == 0:
        print useage_text
    elif command.strip().find('pa') == 0:
        print_msgs(True)
    elif command.strip().find('p') == 0:
        print_msgs()
    elif command.strip().find('rg') == 0:
        matchObj = re.match(r'\s*(\S+)\s+(\S+)\s+(.*)', command, re.M | re.I)
        target_group = matchObj.group(2)
        msg_content = matchObj.group(3)
        itchat.send_msg(msg_content, find_group_name_by_index(int(target_group)))
    elif command.strip().find('r') == 0:
        matchObj = re.match(r'\s*(\S+)\s+(\S+)\s+(.*)', command, re.M | re.I)
        target_user = matchObj.group(2)
        msg_content = matchObj.group(3)
        itchat.send_msg(msg_content, find_friend_name_by_index(int(target_user)))
    elif command.strip().find('g') == 0:
        matchObj = re.match(r'\s*(\S+)\s+(\S+)', command, re.M | re.I)
        target_user = matchObj.group(2)
        print find_friend_name_by_index(int(target_user))
    else:
        print('Unknown command: %s' % command)
        print(useage_text)

