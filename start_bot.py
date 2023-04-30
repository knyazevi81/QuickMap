import multiprocessing
import time
from colorama import Fore, init
import os


def process1():
    os.system('python bot/main.py')


def process2():
    os.system('python bot/up_notif.py')


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=process1)
    p2 = multiprocessing.Process(target=process2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()