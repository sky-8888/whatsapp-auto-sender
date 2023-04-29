# def func(x):
#     return x + 1


# def test_answer():
#     assert func(3) == 4

from main import get_sleep_time
import datetime


def test_start_before_send_hour():
    time = datetime.datetime(2021, 1, 1, 6, 30, 0)
    send_hour = 7
    sleep_time, sleep_until = get_sleep_time(send_hour, time)
    # assert (sleep_until.day, sleep_until.hour) == (1, 7)
    assert sleep_until.day == 1
    assert sleep_until.hour == 7
    assert sleep_until.minute <= 10


def test_start_after_send_hour():
    time = datetime.datetime(2021, 1, 1, 8, 0, 0)
    send_hour = 7
    sleep_time, sleep_until = get_sleep_time(send_hour, time)
    # assert (sleep_until.day, sleep_until.hour) == (2, 7)
    assert sleep_until.day == 2
    assert sleep_until.hour == 7


def test_start_at_send_hour():
    time = datetime.datetime(2021, 1, 1, 7, 30, 0)
    send_hour = 7
    sleep_time, sleep_until = get_sleep_time(send_hour, time)
    # assert (sleep_until.day, sleep_until.hour) == (2, 7)
    assert sleep_until.day == 2
    assert sleep_until.hour == 7
    assert sleep_until.minute <= 10


def test_sunday_before_send_hour():
    time = datetime.datetime(2023, 4, 30, 6, 0, 0)
    send_hour = 7
    sleep_time, sleep_until = get_sleep_time(send_hour, time)
    # assert (sleep_until.day, sleep_until.hour) == (2, 7)
    assert sleep_until.day == 1
    assert sleep_until.hour == 7


def test_sunday_after_send_hour():
    time = datetime.datetime(2023, 4, 30, 8, 0, 0)
    send_hour = 7
    sleep_time, sleep_until = get_sleep_time(send_hour, time)
    # assert (sleep_until.day, sleep_until.hour) == (2, 7)
    assert sleep_until.day == 1
    assert sleep_until.hour == 7


def test_saturday_before_send_hour():
    time = datetime.datetime(2023, 4, 29, 6, 0, 0)
    send_hour = 7
    sleep_time, sleep_until = get_sleep_time(send_hour, time)
    assert sleep_until.day == 1
    assert sleep_until.hour == 7


def test_saturday_after_send_hour():
    time = datetime.datetime(2023, 4, 29, 11, 0, 0)
    send_hour = 7
    sleep_time, sleep_until = get_sleep_time(send_hour, time)
    assert sleep_until.day == 1
    assert sleep_until.hour == 7
