import thread
import itchat, time
from itchat.content import *


@itchat.msg_register(TEXT, isGroupChat=True)
def receive_group_msg(msg):
    print('received group msg.')

@itchat.msg_register(TEXT, isFriendChat=True)
def receive_friend_msg(msg):
    print('received friend msg.')

itchat.auto_login(True)
thread.start_new_thread(itchat.run(), (True, True))
print('here')
while 1:
    command = input()
    print(command)