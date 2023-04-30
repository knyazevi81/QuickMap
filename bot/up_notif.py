import notifiers
import config
import time


def up_notification():
    while True:
        telegram = notifiers.get_notifier('telegram')
        time.sleep(5)
        telegram.notify(token=config.tele_token, chat_id=782697565, message='test notifier!')


if __name__ == '__main__':
    up_notification()