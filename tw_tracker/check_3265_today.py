# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import yfinance as yf
from FinMind.data import DataLoader
from tw_real_broker_data import fetch_real_broker_data

t = yf.Ticker('3265.TWO')
h = t.history(period='5d')
print('=== 台星科 (3265) 近 5 日價量 (含今日 2026-10-06) ===')
print(h[['Open', 'High', 'Low', 'Close', 'Volume']])

dl = DataLoader()
df = dl.taiwan_stock_institutional_investors(stock_id='3265', start_date='2026-09-30', end_date='2026-10-07')
print('\n=== 台星科 近日法人買賣超 ===')
for d in sorted(df['date'].unique()):
    sub = df[df['date'] == d]
    f = sub[sub['name'] == 'Foreign_Investor']
    f_net = (f['buy'].iloc[0] - f['sell'].iloc[0]) / 1000 if not f.empty else 0
    t_row = sub[sub['name'] == 'Investment_Trust']
    t_net = (t_row['buy'].iloc[0] - t_row['sell'].iloc[0]) / 1000 if not t_row.empty else 0
    d_row = sub[sub['name'] == 'Dealer_self']
    d_net = (d_row['buy'].iloc[0] - d_row['sell'].iloc[0]) / 1000 if not d_row.empty else 0
    print(f'{d}: 外資={f_net:+.1f}張, 投信={t_net:+.1f}張, 自營={d_net:+.1f}張')

res = fetch_real_broker_data('3265')
print('\n=== 台星科 今日真實買超 TOP 10 ===')
if res:
    for idx, b in enumerate(res.get('buy_top', [])[:10], 1):
        print(f"{idx:02d}. {b['broker']}: 買進 {b['buy_shares']} 張, 賣出 {b['sell_shares']} 張, 淨買超 {b['net_shares']} 張")
    print('\n=== 台星科 今日真實賣超 TOP 10 ===')
    for idx, s in enumerate(res.get('sell_top', [])[:10], 1):
        print(f"{idx:02d}. {s['broker']}: 買進 {s['buy_shares']} 張, 賣出 {s['sell_shares']} 張, 淨賣超 {s['net_shares']} 張")
