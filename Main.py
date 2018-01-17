import itchat
import time

if __name__ == '__main__':
    itchat.login(enableCmdQR=True)
    while 1:
        time.sleep(10)
        print('pulling msg')
        itchat.pull()
