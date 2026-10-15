# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from FinMind.data import DataLoader
import pandas as pd

dl = DataLoader()
stock_id = '5234'

# 查詢 2026 年 投信 (Investment_Trust) 買賣超
try:
    df = dl.taiwan_stock_institutional_investors(stock_id=stock_id, start_date='2026-01-01', end_date='2026-10-01')
    if not df.empty:
        it = df[df['name'] == 'Investment_Trust']
        print(f"=== 2026 年 投信在 達興材料 ({stock_id}) 的交易總覽 ===")
        print(f"投信有交易的天數: {len(it[it['buy'] + it['sell'] > 0])} 天")
        total_buy = it['buy'].sum()
        total_sell = it['sell'].sum()
        net = (total_buy - total_sell) / 1000
        print(f"2026 累計投信買進: {total_buy/1000:,.1f} 張 | 賣出: {total_sell/1000:,.1f} 張 | 累計淨買賣超: {net:+,.1f} 張")
        
        # 顯示投信有動作的近期交易日
        active_it = it[it['buy'] + it['sell'] > 0]
        if not active_it.empty:
            print("\n近期投信有動作的明細：")
            for idx, r in active_it.tail(15).iterrows():
                net_day = (r['buy'] - r['sell']) / 1000
                print(f"{r['date']} | 買進: {r['buy']/1000:6.1f} 張 | 賣出: {r['sell']/1000:6.1f} 張 | 淨買超: {net_day:+6.1f} 張")
        else:
            print("投信在 2026 年幾無動作。")
except Exception as e:
    print("Error querying Investment_Trust:", e)
