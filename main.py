import thread
import re, time
import itchat
import sys
from itchat.content import *

reload(sys)
sys.setdefaultencoding('utf8')

friend_msgs = {}
group_msgs = {}
in_chatting = False
chatting_target = ''


def enqueue_friend_msg(msg):
    insert_flag = False
    for user in friend_msgs:
        if user == msg['User']['UserName']:
            friend_msgs[user]['msgs'] += [msg]
            friend_msgs[user]['unreadAmount'] += 1
            insert_flag = True
            if in_chatting and chatting_target[:1] != 'g' and find_friend_name_by_index(chatting_target) == user:
                print('%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['CreateTime'])), my_align(friend_msgs[user]['displayName'], 16), msg['Text']))
                pass
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
            if in_chatting and chatting_target[:1] == 'g' and find_group_name_by_index(chatting_target[1:]) == group:
                print('%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['CreateTime'])), my_align(group_msgs[group]['displayName'], 16), msg['Text']))
                pass
            break
    if not insert_flag:
        # it is a new msg which was not enqueue before
        group_msgs[msg['User']['UserName']] = {'displayName': msg['User']['NickName'], 'msgs': [msg], 'unreadAmount': 1}


def print_friend_msgs(count=10, show_history=False, show_latest=False, specific_ref=None):
    specific_user_name = '' if specific_ref is None else find_friend_name_by_index(specific_ref)
    print('====Friend Messages==============')
    for user_name in friend_msgs:
        if specific_user_name == '':
            pass
        elif specific_user_name == user_name:
            pass
        else:
            continue
        print('%s-----(%s):' % (friend_msgs[user_name]['displayName'], find_friend_index_by_name(user_name)))
        if show_history:
            start_position = 0
        elif show_latest:
            start_position = len(friend_msgs[user_name]['msgs']) - friend_msgs[user_name]['unreadAmount']
        else:
            if len(friend_msgs[user_name]['msgs']) < count:
                start_position = 0
            else:
                start_position = len(friend_msgs[user_name]['msgs']) - count
        for i, val in enumerate(friend_msgs[user_name]['msgs'][start_position:]):
            if val['User']['UserName'] == val['FromUserName']:
                print('%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(val['CreateTime'])), my_align(friend_msgs[user_name]['displayName'], 16), val['Text']))
            else:
                print('%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(val['CreateTime'])), my_align(u'\u6211', 16), val['Text']))
        if show_latest:
            friend_msgs[user_name]['unreadAmount'] = 0
        # print line
        print


def print_group_msgs(count=10, show_history=False, show_latest=False, specific_ref=None):
    specific_group_name = '' if specific_ref is None else find_group_name_by_index(specific_ref)
    print('====Group Messages===============')
    for group_name in group_msgs:
        if specific_group_name == '':
            pass
        elif specific_group_name == group_name:
            pass
        else:
            continue
        print('%s-----(%s):' % (group_msgs[group_name]['displayName'], find_group_index_by_name(group_name)))
        if show_history:
            start_position = 0
        elif show_latest:
            start_position = len(group_msgs[group_name]['msgs']) - group_msgs[group_name]['unreadAmount']
        else:
            if len(group_msgs[group_name]['msgs']) < count:
                start_position = 0
            else:
                start_position = len(group_msgs[group_name]['msgs']) - count
        for i, val in enumerate(group_msgs[group_name]['msgs'][start_position:]):
            if val['User']['UserName'] == val['FromUserName']:
                print('%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(val['CreateTime'])), my_align(val['ActualNickName'], 16), val['Text']))
            else:
                print('%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(val['CreateTime'])), my_align(u'\u6211', 16), val['Text']))
        if show_latest:
            group_msgs[group_name]['unreadAmount'] = 0
        # print line
        print


def find_friend_index_by_name(user_name):
    for i, val in enumerate(itchat.originInstance.memberList):
        if user_name == val['UserName']:
            return i


def find_friend_name_by_index(user_index):
    if isinstance(user_index, str):
        user_index = int(user_index)
    return itchat.originInstance.memberList[user_index]['UserName']


def find_group_index_by_name(group_name):
    for i, val in enumerate(itchat.originInstance.chatroomList):
        if group_name == val['UserName']:
            return i


def find_group_name_by_index(group_index):
    if isinstance(group_index, str):
        group_index = int(group_index)
    return itchat.originInstance.chatroomList[group_index]['UserName']


def print_msgs(count=10, show_history=False, show_latest=False):
    print_friend_msgs(count, show_history, show_latest, specific_ref=None)
    print_group_msgs(count, show_history, show_latest, specific_ref=None)


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
    # print(msg)
    # print('received group msg.')


@itchat.msg_register(TEXT, isFriendChat=True)
def receive_friend_msg(msg):
    enqueue_friend_msg(msg)
    # print(msg)
    # print(msg['Text'])
    # print('received friend msg.')


itchat.auto_login(True)
thread.start_new_thread(itchat.run, ())
useage_text = 'Usage:\n' \
              '    p [count:default = 10]         (pull latest [count] messages for each conversation\n' \
              '                       with "member ref" witch is used for reply)\n' \
              '    pl         (pull all latest unread messages with "member ref" witch is used for reply)\n' \
              '    pa         (pull all cached historic messages with "member ref" witch is used for reply)\n' \
              '    enter [target user ref]\n' \
              '               (enter chat transaction with specific friend)\n' \
              '    enter g[target user ref]\n' \
              '               (enter chat transaction with specific group)\n' \
              '    rg [target group ref] [message content]\n' \
              '               (reply message to specific group,\n' \
              '                e.g. reply 0 where are you?)\n' \
              '    r [target user ref] [message content]\n' \
              '               (reply message to specific user,\n' \
              '                e.g. reply 1 where are you?)\n' \
              '    h          (show help menu)'
while 1:
    command = raw_input()
    if in_chatting:
        if command.strip().find('exit') == 0:
            in_chatting = False
            print('Returned to menu model.')
        else:
            if chatting_target.find('g') == 0:
                msg_obj = {'User': {'UserName': find_group_name_by_index(chatting_target[1:])}, 'FromUserName': 'dummy','CreateTime': int(time.time()), 'Text': command}
                itchat.send_msg(command, find_group_name_by_index(chatting_target[1:]))
                pass
            else:
                msg_obj = {'User': {'UserName': find_friend_name_by_index(chatting_target)}, 'FromUserName': 'dummy', 'CreateTime': int(time.time()), 'Text': command}
                itchat.send_msg(command, find_friend_name_by_index(chatting_target))
                pass
    else:
        if command.strip().find('h') == 0:
            print useage_text
        elif command.strip().find('pa') == 0:
            print_msgs(show_history=True)
        elif command.strip().find('pl') == 0:
            print_msgs(show_latest=True)
        elif command.strip().find('p') == 0:
            print_msgs()
        elif command.strip().find('rg') == 0:
            re_obj = re.match(r'\s*(\S+)\s+(\S+)\s+(.*)', command, re.M | re.I)
            if re_obj:
                target_group = re_obj.group(2)
                msg_content = re_obj.group(3)
                msg_obj = {'User': {'UserName': find_group_name_by_index(int(target_group))}, 'FromUserName': 'dummy','CreateTime': int(time.time()), 'Text': msg_content}
                enqueue_group_msg(msg_obj)
                itchat.send_msg(msg_content, find_group_name_by_index(int(target_group)))
            else:
                print('Unknown command: %s' % command)
                print(useage_text)
        elif command.strip().find('r') == 0:
            re_obj = re.match(r'\s*(\S+)\s+(\S+)\s+(.*)', command, re.M | re.I)
            if re_obj:
                target_user = re_obj.group(2)
                msg_content = re_obj.group(3)
                msg_obj = {'User':{'UserName':find_friend_name_by_index(int(target_user))}, 'FromUserName':'dummy', 'CreateTime':int(time.time()), 'Text':msg_content}
                enqueue_friend_msg(msg_obj)
                itchat.send_msg(msg_content, find_friend_name_by_index(int(target_user)))
            else:
                print('Unknown command: %s' % command)
                print(useage_text)
        elif command.strip().find('enter') == 0:
            re_obj = re.match(r'\s*(\S+)\s+(g*\d+)(.*)', command, re.M | re.I)
            if re_obj:
                chatting_target = re_obj.group(2)
                in_chatting = True
                print('Enter "exit" to exit.')
                if chatting_target[:1] == 'g':
                    print_group_msgs(show_history=True, specific_ref=int(chatting_target[1:]))
                    pass
                else:
                    print_friend_msgs(show_history=True, specific_ref=int(chatting_target))
                    pass
            else:
                print('Unknown command: %s' % command)
                print(useage_text)
        else:
            print('Unknown command: %s' % command)
            print(useage_text)

