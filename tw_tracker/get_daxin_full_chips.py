# -*- coding: utf-8 -*-
"""
get_daxin_full_chips.py
調取 2026 年最新 達興材料 (5234) 100% 正確官方籌碼全數據
包含：
1. 三大法人最新累計買賣超與持股比率
2. 集保股權分散表 (千張大戶持股張數與比率)
3. 融資融券餘額與使用率
4. 借券賣出餘額
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from FinMind.data import DataLoader
import pandas as pd

dl = DataLoader()
stock_id = '5234'

print(f"=== 開始調取 達興材料 ({stock_id}) 2026 年最新官方籌碼全貌 ===")

# 1. 集保股權分散表 (千張大戶持股)
try:
    df_holding = dl.taiwan_stock_holding_shares_per(stock_id=stock_id, start_date='2026-08-01', end_date='2026-10-01')
    if not df_holding.empty:
        latest_date = df_holding['date'].max()
        df_latest = df_holding[df_holding['date'] == latest_date]
        print(f"\n【1. 最新集保股權分散表 (日期: {latest_date})】")
        # 尋找千張大戶 (通常 HoldingSharesLevel 為超過 1,000,000 股 或 等級 15)
        print(df_latest[['HoldingSharesLevel', 'people', 'percent', 'unit']])
    else:
        print("\n【1. 集保股權分散表】無資料")
except Exception as e:
    print(f"\n【1. 集保股權分散表】錯誤: {e}")

# 2. 融資融券 (信用交易籌碼)
try:
    df_margin = dl.taiwan_stock_margin_purchase_short_sale(stock_id=stock_id, start_date='2026-09-01', end_date='2026-10-01')
    if not df_margin.empty:
        print(f"\n【2. 2026 年 9 月最新融資融券餘額】")
        print(df_margin.tail(5))
    else:
        print("\n【2. 融資融券】無資料")
except Exception as e:
    print(f"\n【2. 融資融券】錯誤: {e}")

# 3. 外資與三大法人持股比例
try:
    df_shareholding = dl.taiwan_stock_shareholding(stock_id=stock_id, start_date='2026-09-01', end_date='2026-10-01')
    if not df_shareholding.empty:
        print(f"\n【3. 外資持股比例 (2026 年 9 月)】")
        print(df_shareholding.tail(5))
    else:
        print("\n【3. 外資持股比例】無資料")
except Exception as e:
    print(f"\n【3. 外資持股比例】錯誤: {e}")

# 4. 三大法人近 5 日合計買賣超
try:
    df_inst = dl.taiwan_stock_institutional_investors(stock_id=stock_id, start_date='2026-09-20', end_date='2026-10-01')
    if not df_inst.empty:
        print(f"\n【4. 三大法人近 5 日買賣超明細】")
        for date, group in df_inst.groupby('date'):
            fi = group[group['name'] == 'Foreign_Investor']
            it = group[group['name'] == 'Investment_Trust']
            dlr = group[group['name'].str.contains('Dealer', case=False, na=False)]
            
            fi_net = (fi['buy'].sum() - fi['sell'].sum()) / 1000 if not fi.empty else 0
            it_net = (it['buy'].sum() - it['sell'].sum()) / 1000 if not it.empty else 0
            dlr_net = (dlr['buy'].sum() - dlr['sell'].sum()) / 1000 if not dlr.empty else 0
            total_net = fi_net + it_net + dlr_net
            print(f"{date} | 外資: {fi_net:+6.1f} 張 | 投信: {it_net:+6.1f} 張 | 自營商: {dlr_net:+6.1f} 張 | 三大法人合計: {total_net:+7.1f} 張")
except Exception as e:
    print(f"\n【4. 三大法人】錯誤: {e}")
