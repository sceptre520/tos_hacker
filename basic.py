from time import sleep
import csv
from typing import cast
from td.client import TDClient
import db_conn

TDSession = TDClient(
    client_id='UGPAX5IGKEO3JRPGAEQMS4CCNH4I6GPC',
    redirect_uri='http://127.0.0.1:3000',
    credentials_path='token.json'
)
TDSession.login()

def getOneStock(symbol):
    opt_chain = {
        'symbol': symbol,
        'includeQuotes': True,
    }
    option_chains = TDSession.get_options_chain(option_chain=opt_chain)
    stock_id = db_conn.saveStock(option_chains['underlying'])
    print(option_chains['underlying'])
    # ret_symbol = option_chains['underlying']
    # print(ret_symbol)
    for y in option_chains['callExpDateMap']:
        k = option_chains['callExpDateMap'][y]
        for z in k:
            # print(k[z][0]['symbol'])
            db_conn.saveOption(stock_id, k[z][0])


def catchData():
    symbols = []
    with open('std.csv', 'r') as file:
        reader = csv.reader(file)
        i=0
        for row in reader:
            i = i + 1
            if i==1:
                continue
            symbols.append(row[0])
    
    try:
        filer = open("call.log","r")
        keyv = filer.read()
        filer.close()
    except:
        keyv = ''

    index = 0
    ti = 0
    for x in symbols:
        if x == keyv:
            index = ti
        ti = ti + 1
    print('----------')
    print(index)
    
    lenv = len(symbols)
    while(True):
        cur_symbol = symbols[index]

        print(cur_symbol)
        getOneStock(cur_symbol)

        fileh = open("call.log","w+")
        fileh.flush()
        fileh.write(cur_symbol)
        fileh.close()
        index = index + 1
        index = index % lenv
        sleep(1)


catchData()