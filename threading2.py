import os
import threading   
from time import sleep 
from threading import Thread
from threading import Event
from pynput import keyboard


e = threading.Event()
def count():
    while True:
        if e.is_set() == False:
            print("test1")
            sleep(1)
            print("test2")
            sleep(1)
            print("test3")
            sleep(1)
            print("test4")
            sleep(1)
            print("test5")
            sleep(1)
            os.system('clear')
        else:
            print("kablooyey!")

def set_event():
    e.set()


def on_press(a):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

t1 = Thread(target=count)
t1.start()
