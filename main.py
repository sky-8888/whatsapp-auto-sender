import datetime
import os
import time
import random
from whatsapp import check_is_new_user, send_message, whatsapp_init
import holidays


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


def is_today_holiday():
    now = datetime.datetime.now()
    hk_holidays = holidays.HK(years=now.year)  # type: ignore
    for holiday in hk_holidays:
        today = now.strftime("%Y-%m-%d")
        if today == holiday.strftime("%Y-%m-%d"):
            return True
    return False


def start_message_loop(
    send_hour: int, group_id: str, messages: list, user_data_dir: str
):
    while True:
        now = datetime.datetime.now()
        # get sleep time
        sleep_time, sleep_until = get_sleep_time(send_hour, now)

        # check if current time is same as sleep_until
        while now < sleep_until:
            time_till = sleep_until - now
            # print as log
            print(
                f"{now.strftime('%Y-%m-%d %H:%M:%S')} - Sleeping for {time_till.seconds} seconds until {sleep_until.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            # sleep for 10 seconds
            time.sleep(10)
            now = datetime.datetime.now()

        # send message
        if not is_today_holiday():
            send_message(group_id, random.choice(messages), user_data_dir)
            time.sleep(10)


if __name__ == "__main__":
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

    dir_path = os.getcwd()
    user_data_dir = f"{dir_path}/selenium"
    new_user = check_is_new_user(user_data_dir)
    if new_user:
        whatsapp_init(user_data_dir)
    group_id = input("Enter group id: ")

    try:
        send_hour = int(input("Enter send hour: "))
    except ValueError:
        send_hour = 7

    if send_hour < 0:
        send_message(group_id, random.choice(messages), user_data_dir)
        exit(0)
    start_message_loop(send_hour, group_id, messages, user_data_dir)
    # send_message(group_id, random.choice(messages))
