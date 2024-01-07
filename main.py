import argparse
import logging
import os
import sys
import datetime as dt
from helper import config_logging, convert_url, download_file, add_nc_file, re_download_nc_file

if __name__ == '__main__':
    config_logging()

    parser = argparse.ArgumentParser(description="A program that takes option, file numbers, start date and end date as input (e.g. python main.py -o 'download' -f '1,2,3,4' -s '2023-09-20' -e '2023-10-03)")

    # Add arguments for option, file numbers, start date, end date
    parser.add_argument(
        "-o", 
        "--option", 
        help="Input option (redownload or download)", 
        type=str
    )
    parser.add_argument(
        "-f", 
        "--files", 
        help="Input file numbers (1: 'WEBPXTICK_DT.zip', 2: 'TickData_structure.dat', 3: 'TC.txt', 4: 'TC_structure.dat'). Multiple file numbers can be entered at once, separated by commas (e.g. 1,2,3,4)", 
        type=str
    )
    parser.add_argument(
        "-s", 
        "--start", 
        help="Input start date in yyyy-mm-dd format (e.g. 2023-10-03)", 
        type=str
    )
    parser.add_argument(
        "-e", 
        "--end", 
        help="Input end date in yyyy-mm-dd format (e.g. 2023-10-03)", 
        type=str
    )

    args = parser.parse_args()

    if args.option is None:
        args.option = input('Input option (redownload or download): ')

    if args.option == 'redownload':
        re_download_nc_file()

    elif args.option == 'download':
        if args.files is None:
            args.files = input('Input file numbers: ')
        if args.start is None:
            args.start = input('Input start date in yyyy-mm-dd format: ')
        if args.end is None:
            args.end = input('Input end date in yyyy-mm-dd format: ')
        
        # Check if start date, end date valid or not
        try:
            start_date = dt.datetime.strptime(args.start, '%Y-%m-%d').date()
            end_date = dt.datetime.strptime(args.end, '%Y-%m-%d').date()
        except ValueError:
            print('Start date {0} or end date {1} is not valid'.format(args.start, args.end))
            sys.exit()

        args.files = args.files.replace(',','')

        #Start downloading files from start date to end date
        while start_date <= end_date:
            if start_date.weekday() < 5:
                download_dir= r'{0}/downloads/{1}'.format(os.getcwd(),start_date.strftime('%Y-%m-%d'))
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
                
                for i in args.files:
                    i = int(i)
                    url = convert_url(i, start_date)
                    try:
                        logging.info('Downloading file from URL: {0} ({1})'.format(url, start_date.strftime('%Y-%m-%d')))
                        is_completed = download_file(url, download_dir)
                        if (is_completed):
                            logging.info('Completed downloading file from URL: {0} ({1})'.format(url, start_date.strftime('%Y-%m-%d')))
                        else:
                            add_nc_file(url, start_date.strftime('%Y-%m-%d'))
                            logging.info('Not completed downloading file from URL: {0} ({1})'.format(url, start_date.strftime('%Y-%m-%d')))
                    except Exception as e:
                        logging.error('Error downloading {0} ({1}): {2}'.format(url, start_date.strftime('%Y-%m-%d'), e))
            else:
                logging.info('Date {} is a weekend.'.format(start_date.strftime('%Y-%m-%d')))
            start_date = start_date + dt.timedelta(days=1)
    else:
        print('Option is not valid')
