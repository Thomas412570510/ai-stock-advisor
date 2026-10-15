# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import ssl, urllib.request, json

ctx = ssl._create_unverified_context()
url = 'https://openapi.twse.com.tw/v1/exchangeReport/FMTQIK'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    last = data[-1]
    date_roc = last['Date']
    y = int(date_roc[:3]) + 1911
    m = date_roc[3:5]
    d = date_roc[5:7]
    vol_shares = int(last['TradeVolume'])
    val_ntd = int(last['TradeValue'])
    tx = int(last['Transaction'])
    taiex = last['TAIEX']
    chg = last['Change']
    
    print(f"官方發布最新交易日：民國 {date_roc[:3]} 年 {m} 月 {d} 日（西元 {y}-{m}-{d}）")
    print(f"1. 集中市場總成交金額：{val_ntd:,} 元（約 {val_ntd/1e8:.2f} 億元）")
    print(f"2. 集中市場總成交股數：{vol_shares:,} 股（約 {vol_shares/1e3:,.0f} 股 / {vol_shares/1000:,.0f} 張）")
    print(f"3. 總成交筆數：{tx:,} 筆")
    print(f"4. 加權指數收盤：{taiex} 點（漲跌 {chg} 點）")
