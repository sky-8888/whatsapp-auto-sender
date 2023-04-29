import datetime
import os
import time
import random
from whatsapp import check_is_new_user, send_message, whatsapp_init


def get_sleep_time(send_hour: int, now: datetime.datetime):
    # sleep until 7am tomorrow
    sleep_time = 0
    # sleep until monday 7am if today is saturday
    if now.weekday() == 5:
        sleep_time = (24 - now.hour + send_hour + 24) * 60 * 60
    # sleep until monday 7am if today is sunday and it's before 7am
    elif now.weekday() == 6 and now.hour < send_hour:
        sleep_time = (24 - now.hour + send_hour) * 60 * 60
    elif now.hour < send_hour:
        sleep_time = (send_hour - now.hour) * 60 * 60
    # elif now.hour == send_hour:
    #     if now.minute < 30:
    #         sleep_time = (30 - now.minute) * 60
    else:
        sleep_time = (24 - now.hour + send_hour) * 60 * 60
    # subtract minutes to make it 0
    sleep_time -= now.minute * 60
    # add random minutes between 0 and 10
    sleep_time += random.randint(0, 10) * 60
    sleep_until = now + datetime.timedelta(seconds=sleep_time)
    return sleep_time, sleep_until


def start_message_loop(
    send_hour: int, group_id: str, messages: list, user_data_dir: str
):
    while True:
        now = datetime.datetime.now()
        # get sleep time
        sleep_time, sleep_until = get_sleep_time(send_hour, now)
        print(f"Sleeping until {sleep_until}")
        time.sleep(sleep_time)
        # send message
        send_message(group_id, random.choice(messages), user_data_dir)
        time.sleep(10)


if __name__ == "__main__":
    dir_path = os.getcwd()
    user_data_dir = f"{dir_path}/selenium"
    new_user = check_is_new_user(user_data_dir)
    if new_user:
        whatsapp_init(user_data_dir)
    group_id = input("Enter group id: ")
    send_hour = 7
    # a list of messages saying good morning and asking clients if things are fine
    messages = [
        "Good morning! How is everything today?",
        "Morning all, everything fine today?",
        "Morning, how is everything today?",
        "Good morning, any problems today?",
        "Morning, any problems today?",
        "Morning, any issues today?",
        "Good morning, any issues today?",
        "Hi, any issues today?",
        "Hi, any problems today?",
        "Hi, how is everything today?",
    ]

    start_message_loop(send_hour, group_id, messages, user_data_dir)
    # send_message(group_id, random.choice(messages))
