import thread
import re
import itchat, time
from itchat.content import *


@itchat.msg_register(TEXT, isGroupChat=True)
def receive_group_msg(msg):
    print(msg)
    print('received group msg.')

@itchat.msg_register(TEXT, isFriendChat=True)
def receive_friend_msg(msg):
    print(msg)

    print(msg['Text'])
    print('received friend msg.')

itchat.auto_login(True)
thread.start_new_thread(itchat.run, ())
print('here')
while 1:
    command = raw_input()
    if command.find('help') == 0:
        print 'Usage:\n'\
            '    pull         (pull all unread messages)\n'\
            '    pullall       (pull all unread and cached historic messages)\n'\
            '    reply [target user] [message content]\n'\
            '            (reply message to specific user,\n'\
            '        e.g. reply boss where are you?)\n'\
            '    help         (show help menu)'
    elif command.strip().find('pull') == 0:
        pass
    elif command.strip().find('pullall') == 0:
        pass
    elif command.strip().find('reply') == 0:
        matchObj = re.match(r'\s*(\S+)\s+(\S+)\s+(.*)', command, re.M|re.I)
        pass
    print(command)
