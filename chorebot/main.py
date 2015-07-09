from apscheduler.schedulers.blocking import BlockingScheduler
from chorebot.chores import daily_update
from chorebot.log import setup_logging


def main():
    setup_logging()
    scheduler = BlockingScheduler()
    daily_trigger = dict(
        trigger='cron',
        day_of_week='mon-sat',
        hour='2'
    )
    scheduler.add_job(daily_update, **daily_trigger)
    scheduler.start()

if __name__ == '__main__':
    main()
