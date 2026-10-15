# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from FinMind.data import DataLoader

dl = DataLoader()
df = dl.taiwan_stock_institutional_investors(stock_id='5234', start_date='2026-09-01', end_date='2026-10-01')
fi = df[df['name'] == 'Foreign_Investor']

print("=== 2026 年 9 月 達興材料 (5234) 外資真實買賣超 ===")
for idx, row in fi.iterrows():
    b = row['buy']
    s = row['sell']
    net = (b - s) / 1000
    print(f"{row['date']} | 外資買進: {b:8,d} 股 | 外資賣出: {s:8,d} 股 | 淨買超: {net:+7.1f} 張")
