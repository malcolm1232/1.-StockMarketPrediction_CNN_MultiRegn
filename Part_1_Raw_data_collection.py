import urllib
import os
import requests
import pandas as pd
import bs4 as bs
import time
import datetime
import pytz
import sys
from csv import writer
# Create necessary string for future use
premkt = 'PreMarket'
csv = '.csv'
ndx = 'NDX'

totalprinted = 1
def iprint_ndxfuturetech():
    global totalprinted
    close_file_count = 0
    whiletruecount = 1
    ncount = 1

    #You might vary the code / filename this section allows you to print your filename.
    #This will help facilitate visual access when you have multiple files especially when u run on your own Amazon Web Services or Google Cloud
    programfilename1 = sys.argv[0]
    programfilename2 = programfilename1.split('/')
    programfilename = programfilename2[-1]

    #For Scraping using BeautifulSoup
    url = "https://www.investing.com/indices/nq-100-futures-technical"
    params = {
        'pairID': 8874,
        'period': 60,     #Note this can be changed as shown below
                          # 60,   300,  900,   1800,  3600,   18000,   86400, 'week', 'month'
                          # 1min, 5min, 15min, 30min, Hourly, 5 Hours, Daily, Weekly, Monthly
        'viewType': 'normal'}
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}
    url = 'https://www.investing.com/indices/nq-100-futures-technical'
    r = requests.post(url, data=params, headers=headers)
    soup = bs.BeautifulSoup(r.text, 'html.parser')

    #Create Relevant Files
    #today_dateus : Everytime clock strikes 0000 Hours, create a new file for the next day.
    #Example now its 28 July 2020, child folder name will be 2020-07-28. Once it is the next day, after 0000Hours, new directory 2020-07-29 will be created
    today_dateus = str(datetime.datetime.now(tz=pytz.timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")).split()[0]

    desired_filename = 'Nasdaq 1min' #change to your desired filename on Desktop
    def section0_cr8_desktop_path(input0):
        output0 = "C:/Users/malco/Desktop/{}".format(input0)
        if not os.path.exists(output0):
            os.makedirs(output0)

    def section1_cr8_main_premktfolder_path(input1):
        output1 = "C:/Users/malco/Desktop/{}/{}".format(desired_filename, input1)
        # print('Section1 Creates:', output1)
        return output1

    #If path is not created, create a new directory.
    def section2_cr8main_premktfolder(input2):
        if not os.path.exists(input2):
            os.makedirs(input2)
            print('Section2: Path does not exist, Making Directory...')
            print('Section2: Path Exists as: ', input2)
        else:
            # print('Section2: Path Exists as: ', input2)
            pass

    #Returns csv filename
    def section3_create_csvfname(input5):  # input 4 is ndx
        csvfname = input5 + " " + str(today_dateus) + csv
        # print('Section3: returns CSV filename: ',csvfname)
        return csvfname

    #Concatenating
    def section4_create_csvdirname(input6, input7):  # input6 is fname
        csvdirname = input6 + '/' + '{}'.format(input7)
        # print('Section4: returns CSV path: ',csvdirname)
        return csvdirname

    #If CSV file does not exist, Create one with the relevant Column names
    def section5_create_csv_goodbadbuy(csvdirname, tick):
        if not os.path.exists(csvdirname):
            with open(csvdirname, 'a+', newline='') as csv:
                csvwriter = writer(csv)

                # Column Names
                csvwriter.writerow(['Time', 'Price', 'Clock', 'ValChng', 'Percchng', 'Color of Chng',

                                    'GoldFutTASummary', 'MAsummary', 'MAsummaryBuyVal', 'MAsummarySellVal',
                                    'TechIndSummary', 'TechIndSummaryBuyVal', 'TechIndSummarySellVal',

                                    'PivPointClassic', 'S3Classic', 'S2Classic', 'S1Classic', 'PivPointClassic',
                                    'R1Classic', 'R2Classic', 'R3Classic',
                                    'PivPointFib', 'S3Fib', 'S2Fib', 'S1Fib', 'PivPointFib', 'R1Fib', 'R2Fib',
                                    'R3Fib',
                                    'PivPointCamarilla', 'S3Camarilla', 'S2Camarilla', 'S1Camarilla',
                                    'PivPointCamarilla', 'R1Camarilla', 'R2Camarilla', 'R3Camarilla',
                                    'PivPointWoodies', 'S3Woodies', 'S2Woodies', 'S1Woodies', 'PivPointWoodies',
                                    'R1Woodies', 'R2Woodies', 'R3Woodies',
                                    'PivPointDemark', 'S3Demark', 'S2Demark', 'S1Demark', 'PivPointDemark',
                                    'R1Demark', 'R2Demark', 'R3Demark',

                                    # Tech Indicators
                                    'RSI14', 'TechIndiVal0', 'TechIndiAct0',
                                    'STOCH96', 'TechIndiVal1', 'TechIndiAct1',
                                    'STOCHRSI14', 'TechIndiVal2', 'TechIndiAct2',
                                    'MACD1226', 'TechIndiVal3', 'TechIndiAct3',
                                    'ADX14', 'TechIndiVal4', 'TechIndiAct4',
                                    'WILLIAMR', 'TechIndiVal5', 'TechIndiAct5',
                                    'CC14', 'TechIndiVal6', 'TechIndiAct6',
                                    'ATR14', 'TechIndiVal7', 'TechIndiAct7',
                                    'HighLow14', 'TechIndiVal8', 'TechIndiAct8',
                                    'UltimateOsc', 'TechIndiVal9', 'TechIndiAct9',
                                    'ROC', 'TechIndiVaL10', 'TechIndiAct10',
                                    'BullBearPwr13', 'TechIndiVal11', 'TechIndiAct11',
                                    'TechIndiTableSummary', 'TIBuy', 'TISell', 'TINeutral',

                                    # Moving Averages
                                    'MA5', 'MA5SimplePrice', 'MA5ExponenPrice', 'MA5SimpleBS', 'MA5ExponenBS',
                                    'MA10', 'MA10SimplePrice', 'MA10ExponenPrice', 'MA10SimpleBS', 'MA10ExponenBS',
                                    'MA20', 'MA20SimplePrice', 'MA20ExponenPrice', 'MA20SimpleBS', 'MA20ExponenBS',
                                    'MA50', 'MA50SimplePrice', 'MA50ExponenPrice', 'MA50SimpleBS', 'MA50ExponenBS',
                                    'MA100', 'MA100SimplePrice', 'MA100ExponenPrice', 'MA100SimpleBS',
                                    'MA100ExponenBS',
                                    'MA200', 'MA200SimplePrice', 'MA200ExponenPrice', 'MA200SimpleBS',
                                    'MA200ExponenBS',

                                    'MABuy', 'MASell','MATableSummary'])

    ndx_folder_name = '5. Nasdaq Future Tech 1 min'

    #Utilise functions above
    section0_cr8_desktop_path(desired_filename) # make file
    fname1 = section1_cr8_main_premktfolder_path(today_dateus)
    section2_cr8main_premktfolder(fname1)
    csvfname1 = section3_create_csvfname(ndx_folder_name)
    csvdirname1 = section4_create_csvdirname(fname1, csvfname1)
    section5_create_csv_goodbadbuy(csvdirname1, ndx_folder_name)

    timeshort = str(datetime.datetime.now(tz=pytz.timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")).split()[1] #to write time into CSV
    timelongus = str(datetime.datetime.now(tz=pytz.timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")).split() #Visual Access if implementing to Server
    timelongsg = str(datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime("%Y-%m-%d %H:%M:%S")).split() #Visual Access if implementing to Server

    #This will be displayed on server to for visual access of file runtime
    print('                 ___________________________________RUNNING TIMELING________________________')
    print('                 Total Times Printed Since commencement of program:', totalprinted)
    totalprinted += 1
    print('                 whiletrue count', whiletruecount)
    print('                 US Time is:',timelongus)
    print('                 SG Time is:',timelongsg)
    print('                 Latest FileName is:', programfilename)

    #While loop to keep programme running
    if whiletruecount % 10 != 0:
        with open(csvdirname1, 'a+', newline='') as csv1:

            csvwriter1 = writer(csv1)
            # col1: price
            price = soup.find_all('div', class_="top bold inlineblock")[0]
            price = price.find_all('span')[0].text
            col1 = price.replace(',', '')  # price

            got = soup.find('div', class_="bottom lighterGrayFont arial_11")
            col2 = got.find('span').get('class')[1].split('Clock')[0]

            # col 3, 4: change, perentage change
            price = soup.find_all('div', class_="top bold inlineblock")[0]
            col3 = price.find_all('span')[1].text
            col4 = price.find_all('span')[3].text

            # color of change #green or red (indicating market up or down)
            col3tag = price.find_all('span')[1]
            colorofchange = col3tag.get('class')[1].split('Font')[0]

            # col5: SUMMARY
            summary = soup.find_all('div', class_='summary')
            for i in soup.find_all('div', class_="newTechStudiesRight instrumentTechTab"):
                # col1, summary
                col5 = i.find_all('div')[0].text.split(':')[1]

            ## col6,7,8: MA, buy (), sell ()
            sumtable = soup.find_all('div', class_="summaryTableLine")
            summacount = 0
            # print(sumtable)
            for i in sumtable[0]:
                if summacount == 1:
                    col6 = i.text
                if summacount == 2:
                    col7 = i.text.split()[1].split('(')[1].split(')')[0]
                if summacount == 3:
                    col8 = i.text.split()[1].split('(')[1].split(')')[0]
                summacount += 1

            # colcol9, 10, 11: Technical Indicator, buy (), sell ()
            sumtable = soup.find_all('div', class_="summaryTableLine")
            sumticount = 0

            for i in sumtable[1]:
                if sumticount == 1:
                    col9 = i.text
                if sumticount == 2:
                    col10 = i.text.split()[1].split('(')[1].split(')')[0]
                if sumticount == 3:
                    col11 = i.text.split()[1].split('(')[1].split(')')[0]
                sumticount += 1

            # PIVOT POINT PPC 1 to 39

            for i in soup.find_all('table', class_="genTbl closedTbl crossRatesTbl"):
                val = i.find_all('td')
            pivpointcount1 = 0

            # lengthened version forease of viewing.
            # for i in val:
            #     for r in range(40):
            #         if pivpointcount1 == r:
            #             exec(f'ppc{r} = i.text')
            #         pivpointcount1 += 1

            for i in val:
                if pivpointcount1 == 0:
                    ppc0 = i.text
                if pivpointcount1 == 1:
                    ppc1 = i.text
                if pivpointcount1 == 2:
                    ppc2 = i.text
                if pivpointcount1 == 3:
                    ppc3 = i.text
                if pivpointcount1 == 4:
                    ppc4 = i.text
                if pivpointcount1 == 5:
                    ppc5 = i.text
                if pivpointcount1 == 6:
                    ppc6 = i.text
                if pivpointcount1 == 7:
                    ppc7 = i.text
                if pivpointcount1 == 8:
                    ppc8 = i.text
                if pivpointcount1 == 9:
                    ppc9 = i.text
                if pivpointcount1 == 10:
                    ppc10 = i.text
                if pivpointcount1 == 11:
                    ppc11 = i.text
                if pivpointcount1 == 12:
                    ppc12 = i.text
                if pivpointcount1 == 13:
                    ppc13 = i.text
                if pivpointcount1 == 14:
                    ppc14 = i.text
                if pivpointcount1 == 15:
                    ppc15 = i.text
                if pivpointcount1 == 16:
                    ppc16 = i.text
                if pivpointcount1 == 17:
                    ppc17 = i.text
                if pivpointcount1 == 18:
                    ppc18 = i.text
                if pivpointcount1 == 19:
                    ppc19 = i.text
                if pivpointcount1 == 20:
                    ppc20 = i.text
                if pivpointcount1 == 21:
                    ppc21 = i.text
                if pivpointcount1 == 22:
                    ppc22 = i.text
                if pivpointcount1 == 23:
                    ppc23 = i.text
                if pivpointcount1 == 24:
                    ppc24 = i.text
                if pivpointcount1 == 25:
                    ppc25 = i.text
                if pivpointcount1 == 26:
                    ppc26 = i.text
                if pivpointcount1 == 27:
                    ppc27 = i.text
                if pivpointcount1 == 28:
                    ppc28 = i.text
                if pivpointcount1 == 29:
                    ppc29 = i.text
                if pivpointcount1 == 30:
                    ppc30 = i.text
                if pivpointcount1 == 31:
                    ppc31 = i.text
                if pivpointcount1 == 32:
                    ppc32 = i.text
                if pivpointcount1 == 33:
                    ppc33 = i.text
                if pivpointcount1 == 34:
                    ppc34 = i.text
                if pivpointcount1 == 35:
                    ppc35 = i.text
                if pivpointcount1 == 36:
                    ppc36 = i.text
                if pivpointcount1 == 37:
                    ppc37 = i.text
                if pivpointcount1 == 38:
                    ppc38 = i.text
                if pivpointcount1 == 39:
                    ppc39 = i.text
                pivpointcount1 += 1

            # col X to X
            def techtablelong(i, td, class_var, count):
                symbol = i.find_all(td, class_=class_var)[count].text
                return symbol

            #pardon me if code is inefficient here #check how to loop variable
            for i in soup.find_all('table',
                                   class_="genTbl closedTbl technicalIndicatorsTbl smallTbl float_lang_base_1"):
                symbol0 = techtablelong(i, 'td', "first left symbol", 0)
                symbol1 = techtablelong(i, 'td', "first left symbol", 1)
                symbol2 = techtablelong(i, 'td', "first left symbol", 2)
                symbol3 = techtablelong(i, 'td', "first left symbol", 3)
                symbol4 = techtablelong(i, 'td', "first left symbol", 4)
                symbol5 = techtablelong(i, 'td', "first left symbol", 5)
                symbol6 = techtablelong(i, 'td', "first left symbol", 6)
                symbol7 = techtablelong(i, 'td', "first left symbol", 7)
                symbol8 = techtablelong(i, 'td', "first left symbol", 8)
                symbol9 = techtablelong(i, 'td', "first left symbol", 9)
                symbol10 = techtablelong(i, 'td', "first left symbol", 10)
                symbol11 = techtablelong(i, 'td', "first left symbol", 11)

                symbolval0 = techtablelong(i, 'td', "right", 0)
                symbolval1 = techtablelong(i, 'td', "right", 1)
                symbolval2 = techtablelong(i, 'td', "right", 2)
                symbolval3 = techtablelong(i, 'td', "right", 3)
                symbolval4 = techtablelong(i, 'td', "right", 4)
                symbolval5 = techtablelong(i, 'td', "right", 5)
                symbolval6 = techtablelong(i, 'td', "right", 6)
                symbolval7 = techtablelong(i, 'td', "right", 7)
                symbolval8 = techtablelong(i, 'td', "right", 8)
                symbolval9 = techtablelong(i, 'td', "right", 9)
                symbolval10 = techtablelong(i, 'td', "right", 10)
                symbolval11 = techtablelong(i, 'td', "right", 11)

            symbolvalact = i.find_all('span')[0].text

            ##Technical Indicators RSI, Stoch... bull/bear power
            for i in soup.find_all('table',
                                   class_="genTbl closedTbl technicalIndicatorsTbl smallTbl float_lang_base_1"):
                symbolvalact0 = i.find_all('span')[0].text
                symbolvalact1 = i.find_all('span')[1].text
                symbolvalact2 = i.find_all('span')[2].text
                symbolvalact3 = i.find_all('span')[3].text
                symbolvalact4 = i.find_all('span')[4].text
                symbolvalact5 = i.find_all('span')[5].text
                symbolvalact6 = i.find_all('span')[6].text
                symbolvalact7 = i.find_all('span')[7].text
                symbolvalact8 = i.find_all('span')[8].text
                symbolvalact9 = i.find_all('span')[9].text
                symbolvalact10 = i.find_all('span')[10].text
                symbolvalact11 = i.find_all('span')[11].text

            # Summary, Buy, Sell, Neutral
            sum = soup.find_all('p', class_='inlineblock')
            col12 = sum[3].text.split('Summary:')[1].strip()#Summary:
            sum = soup.find_all('td', colspan="3", class_='first left lastRow')[0]
            col13 = sum.find_all('span')[1].text  #Buy
            col14 = sum.find_all('span')[3].text  #Sell
            col15 = sum.find_all('span')[5].text  #Neutral

            count = 0
            matable1 = soup.find_all('table', class_="genTbl closedTbl movingAvgsTbl float_lang_base_2")[0]
            next1c = 0

            for i in matable1:
                count += 1
                if count == 4:
                    td = i.find_all('td')

                    col16 = td[0].text #MA 5
                    col17 = td[1].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # masimple1
                    col18 = td[2].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # maexpo1
                    col19 = td[1].text.split()[1]  # masimplebuysell1
                    col20 = td[2].text.split()[1]  # maexpobuysell1

                    col21 = td[3].text #MA 10
                    col22 = td[4].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # masimple2
                    col23 = td[5].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # maexpo2
                    col24 = td[4].text.split()[1]  # masimplebuysell2
                    col25 = td[5].text.split()[1]  # maexpobuysell2

                    col26 = td[6].text  #MA 20
                    col27 = td[7].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # masimple3
                    col28 = td[8].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # maexpo3
                    col29 = td[7].text.split()[1]  # masimplebuysell3
                    col30 = td[8].text.split()[1]  # maexpobuysell3

                    col31 = td[9].text  #MA 50
                    col32 = td[10].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # masimple4
                    col33 = td[11].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # maexpo4
                    col34 = td[10].text.split()[1]  # masimplebuysell4
                    col35 = td[11].text.split()[1]  # maexpobuysell4

                    col36 = td[12].text  #MA 100
                    col37 = td[13].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # masimple5
                    col38 = td[14].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # maexpo5
                    col39 = td[13].text.split()[1]  # masimplebuysell5
                    col40 = td[14].text.split()[1]  # maexpobuysell5

                    col41 = td[15].text  #MA 200
                    col42 = td[16].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # masimple6
                    col43 = td[17].text.split('Buy')[0].split('Strong Buy')[0].split('Sell')[0].split('Strong Sell')[0].strip()  # maexpo6
                    col44 = td[16].text.split()[1]  # masimplebuysell6
                    col45 = td[17].text.split()[1]  # maexpobuysell6

            # Summary buy, sell, overall summary
            masummary = soup.find_all('td', colspan="3", class_='first left lastRow')[1]

            col46 = masummary.find_all('span')[1].text  # col
            col47 = masummary.find_all('span')[3].text  # col
            masummarybold = soup.find_all('p', class_='inlineblock')
            # print(masummarybold)
            col48 = masummarybold[6].text.split('Summary:')[1].strip()

            csvwriter1.writerow([timeshort, col1, col2, col3, col4, colorofchange, col5,
                                 col6, col7, col8, col9, col10, col11,

                                 # Pivot points Table
                                 ppc0, ppc1, ppc2, ppc3, ppc4, ppc5, ppc6, ppc7,
                                 ppc8, ppc9, ppc10, ppc11, ppc12, ppc13, ppc14, ppc15,
                                 ppc16, ppc17, ppc18, ppc19, ppc20, ppc21, ppc22, ppc23,
                                 ppc24, ppc25, ppc26, ppc27, ppc28, ppc29, ppc30, ppc31,
                                 ppc32, ppc33, ppc34, ppc35, ppc36, ppc37, ppc38, ppc39,

                                 # Technical Indicator
                                 symbol0, symbolval0, symbolvalact0,
                                 symbol1, symbolval1, symbolvalact1,
                                 symbol2, symbolval2, symbolvalact2,
                                 symbol3, symbolval3, symbolvalact3,
                                 symbol4, symbolval4, symbolvalact4,
                                 symbol5, symbolval5, symbolvalact5,
                                 symbol6, symbolval6, symbolvalact6,
                                 symbol7, symbolval7, symbolvalact7,
                                 symbol8, symbolval8, symbolvalact8,
                                 symbol9, symbolval9, symbolvalact9,
                                 symbol10, symbolval10, symbolvalact10,
                                 symbol11, symbolval11, symbolvalact11,
                                 col12, col13, col14, col15,

                                 # Moving Averages
                                 col16, col17, col18, col19, col20,
                                 col21, col22, col23, col24, col25,
                                 col26, col27, col28, col29, col30,
                                 col31, col32, col33, col34, col35,
                                 col36, col37, col38, col39, col40,
                                 col41, col42, col43, col44, col45,
                                 col46, col47, col48])

            all_col = [timeshort, col1, col2, col3, col4, colorofchange, col5,
                       col6, col7, col8, col9, col10, col11,

                       # Pivot points Table
                       ppc0, ppc1, ppc2, ppc3, ppc4, ppc5, ppc6, ppc7,
                       ppc8, ppc9, ppc10, ppc11, ppc12, ppc13, ppc14, ppc15,
                       ppc16, ppc17, ppc18, ppc19, ppc20, ppc21, ppc22, ppc23,
                       ppc24, ppc25, ppc26, ppc27, ppc28, ppc29, ppc30, ppc31,
                       ppc32, ppc3, ppc34, ppc35, ppc36, ppc37, ppc38, ppc39,

                       # Technical Indicator
                       symbol0, symbolval0, symbolvalact0,
                       symbol1, symbolval1, symbolvalact1,
                       symbol2, symbolval2, symbolvalact2,
                       symbol3, symbolval3, symbolvalact3,
                       symbol4, symbolval4, symbolvalact4,
                       symbol5, symbolval5, symbolvalact5,
                       symbol6, symbolval6, symbolvalact6,
                       symbol7, symbolval7, symbolvalact7,
                       symbol8, symbolval8, symbolvalact8,
                       symbol9, symbolval9, symbolvalact9,
                       symbol10, symbolval10, symbolvalact10,
                       symbol11, symbolval11, symbolvalact11,
                       col12, col13, col14, col15,

                       # Moving Averages
                       col16, col17, col18, col19, col20,
                       col21, col22, col23, col24, col25,
                       col26, col27, col28, col29, col30,
                       col31, col32, col33, col34, col35,
                       col36, col37, col37, col39, col40,
                       col41, col42, col43, col44, col45,
                       col46, col47, col48]

            all_col_name =['Time', 'Price', 'Clock', 'ValChng', 'Percchng', 'Color of Chng',

                                    'GoldFutTASummary', 'MAsummary', 'MAsummaryBuyVal', 'MAsummarySellVal',
                                    'TechIndSummary', 'TechIndSummaryBuyVal', 'TechIndSummarySellVal',

                                    'PivPointClassic', 'S3Classic', 'S2Classic', 'S1Classic', 'PivPointClassic',
                                    'R1Classic', 'R2Classic', 'R3Classic',
                                    'PivPointFib', 'S3Fib', 'S2Fib', 'S1Fib', 'PivPointFib', 'R1Fib', 'R2Fib',
                                    'R3Fib',
                                    'PivPointCamarilla', 'S3Camarilla', 'S2Camarilla', 'S1Camarilla',
                                    'PivPointCamarilla', 'R1Camarilla', 'R2Camarilla', 'R3Camarilla',
                                    'PivPointWoodies', 'S3Woodies', 'S2Woodies', 'S1Woodies', 'PivPointWoodies',
                                    'R1Woodies', 'R2Woodies', 'R3Woodies',
                                    'PivPointDemark', 'S3Demark', 'S2Demark', 'S1Demark', 'PivPointDemark',
                                    'R1Demark', 'R2Demark', 'R3Demark',

                                    # Tech Indicators
                                    'RSI14', 'TechIndiVal0', 'TechIndiAct0',
                                    'STOCH96', 'TechIndiVal1', 'TechIndiAct1',
                                    'STOCHRSI14', 'TechIndiVal2', 'TechIndiAct2',
                                    'MACD1226', 'TechIndiVal3', 'TechIndiAct3',
                                    'ADX14', 'TechIndiVal4', 'TechIndiAct4',
                                    'WILLIAMR', 'TechIndiVal5', 'TechIndiAct5',
                                    'CC14', 'TechIndiVal6', 'TechIndiAct6',
                                    'ATR14', 'TechIndiVal7', 'TechIndiAct7',
                                    'HighLow14', 'TechIndiVal8', 'TechIndiAct8',
                                    'UltimateOsc', 'TechIndiVal9', 'TechIndiAct9',
                                    'ROC', 'TechIndiVaL10', 'TechIndiAct10',
                                    'BullBearPwr13', 'TechIndiVal11', 'TechIndiAct11',
                                    'TechIndiTableSummary', 'TIBuy', 'TISell', 'TINeutral',

                                    # Moving Averages
                                    'MA5', 'MA5SimplePrice', 'MA5ExponenPrice', 'MA5SimpleBS', 'MA5ExponenBS',
                                    'MA10', 'MA10SimplePrice', 'MA10ExponenPrice', 'MA10SimpleBS', 'MA10ExponenBS',
                                    'MA20', 'MA20SimplePrice', 'MA20ExponenPrice', 'MA20SimpleBS', 'MA20ExponenBS',
                                    'MA50', 'MA50SimplePrice', 'MA50ExponenPrice', 'MA50SimpleBS', 'MA50ExponenBS',
                                    'MA100', 'MA100SimplePrice', 'MA100ExponenPrice', 'MA100SimpleBS',
                                    'MA100ExponenBS',
                                    'MA200', 'MA200SimplePrice', 'MA200ExponenPrice', 'MA200SimpleBS',
                                    'MA200ExponenBS',

                                    'MATableSummary', 'MABuy', 'MASell']
            ##Unhash to view data
            # for i in range(124):
            #     print('{} is: {}'.format(all_col_name[i], all_col[i] ))

            # time.sleep(1.5)
            # print('sleeping for 1.5')
    else:
        close_file_count +=1
        print('closed file')

count_all_all = 0
while_true_count1 = 0
unable_print = 0

for i in range(0,10000000):
    #while loop to keep it running
    while True:
        try:
            while_true_count1 +=1
            # print('attempting')
            if count_all_all==0:
                tic = time.time()
                iprint_ndxfuturetech() #call your function to get data
                toc = time.time()
                tocketty = toc-tic
                count_all_all+=1
            else:
                tic = time.time()
                iprint_ndxfuturetech()#call your function to get data

                toc = time.time()
                toe=  toc - tic
                print('                 _________________________________')
                print('                 Time Taken to run (Current) program:', toe)
                tocketty = tocketty + toe
                avg_tocky = tocketty/while_true_count1
                print('                 Average time taken:', avg_tocky)
                print('                 TOTAL Time Run (Since Inception):', tocketty)
                print('                 Time Unable to print:', unable_print)

                count_all_all+=1
        except:
            unable_print +=1
            continue
        break