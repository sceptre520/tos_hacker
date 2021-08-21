import sqlite3
from os.path import exists
dbName = "build.db"
def init():
    if not exists(dbName):
        connection = sqlite3.connect(dbName)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE "stock" (
                "id"	INTEGER,
                "symbol"	TEXT,
                "description"	TEXT,
                "change"	TEXT,
                "percentChange"	TEXT,
                "close"	TEXT,
                "quoteTime"	TEXT,
                "tradeTime"	TEXT,
                "bid"	TEXT,
                "ask"	TEXT,
                "last"	TEXT,
                "mark"	TEXT,
                "markChange"	TEXT,
                "markPercentChange"	TEXT,
                "bidSize"	TEXT,
                "askSize"	TEXT,
                "highPrice"	TEXT,
                "lowPrice"	TEXT,
                "openPrice"	TEXT,
                "totalVolume"	TEXT,
                "exchangeName"	TEXT,
                "fiftyTwoWeekHigh"	TEXT,
                "fiftyTwoWeekLow"	TEXT,
                "delayed"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)


        cursor.execute("""
            CREATE TABLE "options" (
                "id"	INTEGER,
                "symbol_id"	INTEGER,
                "putCall"	TEXT,
                "symbol"	TEXT,
                "description"	TEXT,
                "exchangeName"	TEXT,
                "bid"	TEXT,
                "ask"	TEXT,
                "last"	TEXT,
                "mark"	TEXT,
                "bidSize"	TEXT,
                "askSize"	TEXT,
                "bidAskSize"	TEXT,
                "lastSize"	TEXT,
                "highPrice"	TEXT,
                "lowPrice"	TEXT,
                "openPrice"	TEXT,
                "closePrice"	TEXT,
                "totalVolume"	TEXT,
                "tradeDate"	TEXT,
                "tradeTimeInLong"	TEXT,
                "quoteTimeInLong"	TEXT,
                "netChange"	TEXT,
                "volatility"	TEXT,
                "delta"	TEXT,
                "gamma"	TEXT,
                "theta"	TEXT,
                "vega"	TEXT,
                "rho"	TEXT,
                "openInterest"	TEXT,
                "timeValue"	TEXT,
                "theoreticalOptionValue"	TEXT,
                "theoreticalVolatility"	TEXT,
                "optionDeliverablesList"	TEXT,
                "strikePrice"	TEXT,
                "expirationDate"	TEXT,
                "daysToExpiration"	TEXT,
                "expirationType"	TEXT,
                "lastTradingDay"	TEXT,
                "multiplier"	TEXT,
                "settlementType"	TEXT,
                "deliverableNote"	TEXT,
                "isIndexOption"	TEXT,
                "percentChange"	TEXT,
                "markChange"	TEXT,
                "markPercentChange"	TEXT,
                "nonStandard"	TEXT,
                "inTheMoney"	TEXT,
                "mini"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

        connection.commit()

def saveStock(dict):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stock WHERE symbol='{data}';".format(data=dict['symbol']))
    rows = cursor.fetchall()
    if len(rows) == 0:
        col = ''
        val = ''
        for x in dict:
            if col != '':
                col = col + ', '
            if val != '':
                val = val + ', '
            col = col + x
            val = val + '"' + str(dict[x]) + '"'
        print("INSERT INTO stock({col}) VALUES ({val});".format(col=col,val=val))
        cursor.execute("INSERT INTO stock({col}) VALUES ({val});".format(col=col,val=val))
        ret = cursor.lastrowid
    else:
        set_str = ''
        for x in dict:
            if set_str != '':
                set_str = set_str + ', '
            set_str = set_str + x + '="' + str(dict[x]) + '"'
        print("UPDATE stock SET {set_str} WHERE id={id};".format(set_str=set_str,id=rows[0][0]))
        cursor.execute("UPDATE stock SET {set_str} WHERE id={id};".format(set_str=set_str,id=rows[0][0]))
        ret = rows[0][0]
    connection.commit()
    return ret

def saveOption(stock_id, dict):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM options WHERE symbol='{data}' AND symbol_id={symbol_id};".format(data=dict['symbol'], symbol_id=stock_id))
    rows = cursor.fetchall()
    if len(rows) == 0:
        col = 'symbol_id'
        val = str(stock_id)
        for x in dict:
            if x == 'optionDeliverablesList':
                tmp_val = 'x'
            else:
                tmp_val = str(dict[x])
            col = col + ', ' + x
            val = val + ', ' + '"' + tmp_val + '"'
        cursor.execute("INSERT INTO options({col}) VALUES ({val});".format(col=col,val=val))
    else:
        set_str = 'symbol_id='+str(stock_id)
        for x in dict:
            if x == 'optionDeliverablesList':
                tmp_val = 'x'
            else:
                tmp_val = str(dict[x])
            set_str = set_str + ', '  + x + '="' + tmp_val + '"'
        cursor.execute("UPDATE options SET {set_str} WHERE id={id};".format(set_str=set_str,id=rows[0][0]))
    connection.commit()

def scanData(filterV):
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    where = ''
    if filterV['lastmin'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'a.last>=' + filterV['lastmin']
    if filterV['lastmax'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'a.last<=' + filterV['lastmax']
    if filterV['volumemin'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'a.totalVolume>=' + filterV['volumemin']
    if filterV['volumemax'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'a.totalVolume<=' + filterV['volumemax']
    
    if filterV['openinterestmin'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'b.openInterest>=' + filterV['openinterestmin']
    if filterV['openinterestmax'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'b.openInterest<=' + filterV['openinterestmax']
    if filterV['optionvolumemin'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'b.totalVolume>=' + filterV['optionvolumemin']
    if filterV['optionvolumemax'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'b.totalVolume<=' + filterV['optionvolumemax']
    
    if filterV['dtemin'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'b.daysToExpiration>=' + filterV['dtemin']
    if filterV['dtemax'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'b.daysToExpiration<=' + filterV['dtemax']
    if filterV['optLastmin'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'b.last>=' + filterV['optLastmin']
    if filterV['optLastmax'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'b.last<=' + filterV['optLastmax']
    if filterV['optDeltamin'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'b.delta>=' + filterV['optDeltamin']
    if filterV['optDeltamax'] != '':
        if where != '':
            where = where + ' AND '
        where = where + 'b.delta<=' + filterV['optDeltamax']
    
    if where != '':
        where = " WHERE " + where

    cursor.execute("SELECT b.* FROM options b LEFT JOIN stock a ON b.symbol_id=a.id {where} LIMIT 1000;".format(where=where))
    rows = cursor.fetchall()
    ret = []
    for row in rows:
        tmp = {
            'id' : row[0],
            'symbol' : row[3],
            'description' : row[4],
            'last' : row[8],
            'netchg' : row[22],
            'bid' : row[6],
            'ask' : row[7],
            'volume' : row[18],
            'openinterest' : row[29],
            'pcratio' : 'N/A'
        }
        ret.append(tmp)
    connection.commit()
    return ret
