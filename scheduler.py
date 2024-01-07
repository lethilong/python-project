import schedule
import time
from datetime import date, timedelta
import os
import logging
from helper import download_file, convert_url, config_logging, re_download_nc_file



def run(delta):
    today = date.today()
    #Get previous date to download
    download_date = today - timedelta(days=delta)
    download_dir= r'{0}\downloads\{1}'.format(os.getcwd(),download_date.strftime('%Y-%m-%d'))
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for i in range(1, 5):
        url = convert_url(i, download_date)
        try:
            logging.info('Downloading file from URL: {0} ({1})'.format(url, download_date.strftime('%Y-%m-%d')))
            is_completed = download_file(url, download_dir)
            if (is_completed):
                logging.info('Completed downloading file from URL: {0} ({1})'.format(url, download_date.strftime('%Y-%m-%d')))
            else:
                logging.info('Not completed downloading file from URL: {0} ({1})'.format(url, download_date.strftime('%Y-%m-%d')))
        except Exception as e:
            logging.error('Error downloading {0} ({1}): {2}'.format(url, download_date.strftime('%Y-%m-%d'), e))

schedule.every().monday.at("09:00").do(run, 3)
schedule.every().tuesday.at("09:00").do(run, 1)
schedule.every().wednesday.at("09:00").do(run, 1)
schedule.every().thursday.at("09:00").do(run, 1)
schedule.every().friday.at("09:00").do(run, 1)
schedule.every().friday.at("21:00").do(re_download_nc_file)

config_logging()
while True:
    schedule.run_pending()
    time.sleep(5)