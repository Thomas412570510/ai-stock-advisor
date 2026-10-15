# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from tw_real_broker_data import fetch_real_broker_data
import yfinance as yf
import requests

print("=== 6706 惠特 盤後真實分點清單 ===")
res = fetch_real_broker_data("6706")
if res:
    print("\n【買超分點 TOP 15】")
    for idx, b in enumerate(res.get("buy_top", []), 1):
        print(f"{idx:02d}. {b['broker']}: 買進 {b['buy_shares']} 張, 賣出 {b['sell_shares']} 張, 淨買超 {b['net_shares']} 張")
    print("\n【賣超分點 TOP 15】")
    for idx, s in enumerate(res.get("sell_top", []), 1):
        print(f"{idx:02d}. {s['broker']}: 買進 {s['buy_shares']} 張, 賣出 {s['sell_shares']} 張, 淨賣超 {s['net_shares']} 張")

t = yf.Ticker("6706.TW")
h = t.history(period="5d")
print("\n=== 惠特 近 5 日價量 ===")
print(h[["Open", "High", "Low", "Close", "Volume"]])
