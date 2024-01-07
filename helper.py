import logging
import os, requests
import datetime as dt
import csv
import pandas as pd

def config_logging():
    log_dir = 'logging'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(
        filename = f"{log_dir}/logging_{dt.datetime.now().strftime('%Y%m%d')}.log",
        format = '%(asctime)s %(levelname)s %(message)s',
        level = logging.DEBUG,
        datefmt = '%Y-%m-%d %H:%M:%S'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def convert_url(download_file, download_date): 

    # Date 01/12/2020 -> index: 4780   
    start_date = dt.date(2020, 12, 1)
    start_index = 4780
    delta = download_date - start_date
    num_weekend_days = sum(1 for i in range(delta.days + 1) if (start_date + dt.timedelta(i)).weekday() >= 5)
    index = start_index + delta.days - num_weekend_days

    files_dict = {
        1: 'WEBPXTICK_DT.zip', 
        2: 'TickData_structure.dat', 
        3: 'TC.txt', 
        4: 'TC_structure.dat'
    }
    file = files_dict.get(download_file)
        
    url = f'https://links.sgx.com/1.0.0/derivatives-historical/{index}/{file}'
    return url


def download_file(url, download_dir):
    # logging.info('Downloading file from URL: %s' %url)
    response = requests.get(url,stream=True)
    if (response.headers.get('Content-Disposition')): 
        file_name = response.headers.get('Content-Disposition').split('filename=')[1]
        with open(os.path.join(download_dir, file_name), 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        is_completed = os.path.exists(os.path.join(download_dir, file_name))
        return is_completed
    else:
        return False
    
def add_nc_file(url, date):
    with open('nc_file.csv', 'a', newline='') as csv_file:
        csv_file.seek(0, 2)
        writer = csv.writer(csv_file)
        init_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        last_update = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'not completed'
        writer.writerow([date, url, init_time, last_update, status])

def re_download_nc_file():
    df = pd.read_csv('nc_file.csv')
    nc_df = df[df['status'] == 'not completed']
    for i in nc_df.index:
        download_dir = r'{0}/downloads/{1}'.format(os.getcwd(), df['date'][i])
        logging.info('Redownloading file from URL: {0} ({1})'.format(df['url'][i], df['date'][i]))
        is_completed = download_file(df['url'][i], download_dir)
        if (is_completed):
            df.at[i, 'status'] = 'completed'
            df.at[i, 'last_update'] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df.to_csv('nc_file.csv', index=False)
            logging.info('Completed redownloading file from URL: {0} ({1})'.format(df['url'][i], df['date'][i]))
        else:
            logging.info('Not completed redownloading file from URL: {0} ({1})'.format(df['url'][i], df['date'][i]))
        