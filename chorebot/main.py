import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from chorebot.chores import daily_update
from chorebot.log import setup_logging


def main():
    setup_logging()
    scheduler = BlockingScheduler()

    run_now = len(sys.argv) > 1
    if run_now:
        scheduler.add_job(daily_update)
    else:
        scheduler.add_job(
            daily_update,
            trigger='cron',
            day_of_week='mon-sat',
            hour='2',
        )

    scheduler.start()

if __name__ == '__main__':
    main()
