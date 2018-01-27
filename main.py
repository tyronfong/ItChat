import thread
import re
import itchat
from itchat.content import *

friend_msgs = {}
group_msgs = {}


def enqueue_friend_msg(msg):
    insert_flag = False;
    for user in friend_msgs:
        if user == msg['User']['UserName']:
            friend_msgs[user]['msgs'] += [msg]
            friend_msgs[user]['unreadAmount'] += 1
            insert_flag = True
            break
    if not insert_flag:
        # it is a new msg which was not enqueue before
        friend_msgs[msg['User']['UserName']] = {'msgs': [msg], 'unreadAmount': 1}
    pass


def enqueue_group_msg(msg):
    pass


def print_friend_msgs(show_history=False):
    print('====Friend Messages==============')
    for user in friend_msgs:
        init_position = 0 if show_history else (len(friend_msgs[user]['msgs']) - friend_msgs[user]['unreadAmount'])
        for i, val in enumerate(friend_msgs[user]['msgs'], init_position):
            print('%s %-10s: %s' % (val['CreateTime'], val['User']['RemarkName'] if val['User']['RemarkName'] != '' else val['User']['NickName'], val['Text']))
        friend_msgs[user]['unreadAmount'] = 0
    pass


def print_group_msgs(show_history=False):
    print('====Group Messages===============')
    pass


def print_msgs(show_history=False):
    print_friend_msgs(show_history)
    print_group_msgs(show_history)


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
while 1:
    command = raw_input()
    if command.strip().find('help') == 0:
        print 'Usage:\n' \
              '    pull          (pull all unread messages)\n' \
              '    pullall       (pull all unread and cached historic messages)\n' \
              '    reply [target user] [message content]\n' \
              '                  (reply message to specific user,\n' \
              '                   e.g. reply boss where are you?)\n' \
              '    help          (show help menu)'
    elif command.strip().find('pull') == 0:
        print_msgs()
    elif command.strip().find('pullall') == 0:
        print_msgs(True)
    elif command.strip().find('reply') == 0:
        matchObj = re.match(r'\s*(\S+)\s+(\S+)\s+(.*)', command, re.M | re.I)
        target_user = matchObj.group(2)
        msg_content = matchObj.group(3)
        pass
    print(command)
