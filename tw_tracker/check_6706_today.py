# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from tw_real_broker_data import fetch_real_broker_data
from FinMind.data import DataLoader
import yfinance as yf

print("=== 6706 惠特 2026-10-05 今日真實盤後分點 ===")
res = fetch_real_broker_data("6706")
if res:
    print("\n【買超分點 TOP 10】")
    for idx, b in enumerate(res.get("buy_top", [])[:10], 1):
        print(f"{idx:02d}. {b['broker']}: 買進 {b['buy_shares']} 張, 賣出 {b['sell_shares']} 張, 淨買超 {b['net_shares']} 張")
    print("\n【賣超分點 TOP 10】")
    for idx, s in enumerate(res.get("sell_top", [])[:10], 1):
        print(f"{idx:02d}. {s['broker']}: 買進 {s['buy_shares']} 張, 賣出 {s['sell_shares']} 張, 淨賣超 {s['net_shares']} 張")

t = yf.Ticker("6706.TW")
h = t.history(period="5d")
print("\n=== 惠特 近 5 日價量 ===")
print(h[["Open", "High", "Low", "Close", "Volume"]])

print("\n=== 惠特 今日法人買賣超 ===")
dl = DataLoader()
df = dl.taiwan_stock_institutional_investors(stock_id="6706", start_date="2026-09-29", end_date="2026-10-06")
print(df.tail(8))
