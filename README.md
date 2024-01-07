# SGX-Downloader

Design a job to download files daily from SGX website.

## Install requirements
Make sure that python and pip installed on the system. Run one of these command:

```bash
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

## Command

The usage of the scripts and their explaination. 

### Run `main.py`

```
usage: main.py [-h] [-o OPTION] [-f FILES] [-s START] [-e END]

A program that takes option, file numbers, start date and end date as input (e.g. python main.py -o 'download' -f '1,2,3,4' -s '2023-09-20' -e '2023-10-03)        

optional arguments:
  -h, --help            show this help message and exit
  -o OPTION, --option OPTION
                        Input option (redownload or download)
  -f FILES, --files FILES
                        Input file numbers (1: 'WEBPXTICK_DT.zip', 2: 'TickData_structure.dat', 3: 'TC.txt', 4: 'TC_structure.dat'). Multiple file numbers can be  
                        entered at once, separated by commas (e.g. 1,2,3,4)
  -s START, --start START
                        Input start date in yyyy-mm-dd format (e.g. 2023-10-03)
  -e END, --end END     Input end date in yyyy-mm-dd format (e.g. 2023-10-03)
```

#### Example command

- Redownload files not completed (stored in **nc_file.csv**): `python main.py -o 'redownload'`
- Download file TC.txt only between 2 days: `python main.py -o 'download' -f '3' -s '2023-09-20' -e '2023-10-02'`
- Download files between 2 days: `python main.py -o 'download' -f '1,2,3,4' -s '2023-09-20' -e '2023-10-02'`
- Download files of a specific day: `python main.py -o 'download' -f '1,2,3,4' -s '2023-09-20' -e '2023-09-20'`

### Run `scheduler.py`

Run job to download files daily from SGX website: 
`python scheduler.py`

## Structure

```
│   helper.py
│   main.py
│   nc_file.csv
│   README.md
│   requirements.txt
│   scheduler.py
│
├───downloads
│   ├───2023-09-21
│   │       TC_20230921.txt
│   │       TC_structure.dat
│   │       TickData_structure.dat
│   │       WEBPXTICK_DT-20230921.zip
│   │
│   ├───2023-09-22
│   │       TC_20230922.txt
│   │       TC_structure.dat
│   │       TickData_structure.dat
│   │       WEBPXTICK_DT-20230922.zip
│   │
│   ├───2023-09-25
│   │       TC_20230925.txt
│   │       TC_structure.dat
│   │       TickData_structure.dat
│   │       WEBPXTICK_DT-20230925.zip
│   │
│   ├───2023-09-26
│   │       TC_20230926.txt
│   │       TC_structure.dat
│   │       TickData_structure.dat
│   │       WEBPXTICK_DT-20230926.zip
│   │
│   ├───2023-09-27
│   │       TC_20230927.txt
│   │       TC_structure.dat
│   │       TickData_structure.dat
│   │       WEBPXTICK_DT-20230927.zip
│   │
│   ├───2023-09-28
│   │       TC_20230928.txt
│   │       TC_structure.dat
│   │       TickData_structure.dat
│   │       WEBPXTICK_DT-20230928.zip
│   │
│   ├───2023-09-29
│   │       TC_20230929.txt
│   │       TC_structure.dat
│   │       TickData_structure.dat
│   │       WEBPXTICK_DT-20230929.zip
│   │
│   ├───2023-10-02
│   │       TC_20231002.txt
│   │       TC_structure.dat
│   │       TickData_structure.dat
│   │       WEBPXTICK_DT-20231002.zip
│   │
│   └───2023-10-03
│           TC_20231003.txt
│           TC_structure.dat
│           TickData_structure.dat
│           WEBPXTICK_DT-20231003.zip
│
└───logging
        logging_20230929.log
        logging_20231002.log
        logging_20231003.log
        logging_20231004.log
```

## Idea
The website only list files for the past 5 market days. However, I have discovered that the download links for the files follow a specific pattern. I can download files i need with link: `https://links.sgx.com/1.0.0/derivatives-historical/{index}/{file}`
- {index} is is the no of record or can simply call it day_id
- {file} is the general name of file i need to download

e.g. The download link of WEBPXTICK_DT.zip on 03 Oct 2023 is _https://links.sgx.com/1.0.0/derivatives-historical/5520/WEBPXTICK_DT.zip_

### How to calculate {index}

{index} is order of record set that SGX has. I realized:
- index('20230928') = 5517, index('20230929')= 5518, index('20231002') = 5520 => data available only in business (exclude Saturday and Sunday)
- I choose 01 Dec 2020 as start date. index('20201201') = 4780 => index(download_date) = index('20201201) + (download_date - start_date) - num_weekend_days

## Resolve requirements

#### 2. It should be able to download both historical files (files not on today) and today's file based on user's instructions
We can run **main.py** and input start date, end date to download historical files 

#### 3. Logging must be implemented
I have implemented logging functionality to record program information. This is achieved by creating a directory named **logging** if it does not already exist, and storing the log files in this directory. The log file name is set to **logging_<executed_date>.log**, format of executed_date is 'yyyymmdd'. 

#### 4. The recovery plan

- If the downloading failed on one day or on some days, i stored information of missing files in **nc_file.csv**. This csv file contains information about the files that were not successfully downloaded, as indicated by the "not completed" status.I can use it to get information of missing files and redownload these file.

- Is the redownloading automatic or does it require manual intervention?
    > - If **scheduler.py** is running, the redownloading is automatic. The redownloading is executed at 21:00 every friday.    
    > - Another way is running **main.py** with 'redownload' option.

- The website only lists the recent files. Is it possible to download older files?
    > It is possible to download older files with link: `https://links.sgx.com/1.0.0/derivatives-historical/{index}/{file}`