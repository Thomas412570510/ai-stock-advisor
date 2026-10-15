# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from FinMind.data import DataLoader
import pandas as pd

dl = DataLoader()
df = dl.taiwan_stock_month_revenue(stock_id='3265', start_date='2025-01-01', end_date='2026-10-07')

# 整理 2025 與 2026 對照
p2025 = df[df['revenue_year'] == 2025].set_index('revenue_month')['revenue']
p2026 = df[df['revenue_year'] == 2026].set_index('revenue_month')['revenue']

for m in range(1, 13):
    v25 = p2025.get(m, 0)
    v26 = p2026.get(m, 0)
    if v26 > 0 and v25 > 0:
        yoy = (v26 - v25) / v25 * 100
        print(f"2026年 {m:02d}月營收: {v26/1e8:.2f} 億 (2025年同期: {v25/1e8:.2f} 億, YoY: {yoy:+.2f}%)")
    elif v26 > 0:
        print(f"2026年 {m:02d}月營收: {v26/1e8:.2f} 億")
