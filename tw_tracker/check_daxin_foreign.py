# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from FinMind.data import DataLoader
dl = DataLoader()

try:
    # 抓取 5234 (達興材料) 最近一個月的 三大法人 買賣超
    df = dl.taiwan_stock_institutional_investors(stock_id='5234', start_date='2024-09-01', end_date='2024-10-01')
    if not df.empty:
        print("Date | Foreign Buy | Foreign Sell | Net Buy (張)")
        for date, group in df.groupby('date'):
            fi = group[group['name'].str.contains('Foreign|外資', case=False, na=False)]
            if not fi.empty:
                b = fi['buy'].sum()
                s = fi['sell'].sum()
                net = (b - s) / 1000
                print(f"{date} | {b:6,d} | {s:6,d} | {net:+7.1f} 張")
    else:
        print("FinMind returned empty for 5234 institutional investors.")
except Exception as e:
    print('Error:', e)
