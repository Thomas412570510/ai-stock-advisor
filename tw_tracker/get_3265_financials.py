# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import yfinance as yf
import pandas as pd

t = yf.Ticker('3265.TWO')
inc = t.quarterly_income_stmt
print("=== 台星科 (3265) 近 5 季損益表數據 ===")
for col in inc.columns[:5]:
    dt = col.strftime('%Y-%m-%d')
    rev = inc.loc['Total Revenue', col] if 'Total Revenue' in inc.index else 0
    gp = inc.loc['Gross Profit', col] if 'Gross Profit' in inc.index else 0
    op = inc.loc['Operating Income', col] if 'Operating Income' in inc.index else 0
    ni = inc.loc['Net Income', col] if 'Net Income' in inc.index else 0
    eps = inc.loc['Diluted EPS', col] if 'Diluted EPS' in inc.index else 0
    
    gm = (gp / rev * 100) if rev else 0
    opm = (op / rev * 100) if rev else 0
    npm = (ni / rev * 100) if rev else 0
    
    print(f"季度: {dt}")
    print(f"  營收: {rev/1e8:.2f} 億")
    print(f"  毛利: {gp/1e8:.2f} 億 (毛利率: {gm:.2f}%)")
    print(f"  營業利益: {op/1e8:.2f} 億 (營益率: {opm:.2f}%)")
    print(f"  稅後淨利: {ni/1e8:.2f} 億 (淨利率: {npm:.2f}%)")
    print(f"  EPS: {eps:.2f} 元")
    print("---")

bs = t.quarterly_balance_sheet
if not bs.empty:
    col = bs.columns[0]
    cash = bs.loc['Cash Cash Equivalents And Short Term Investments', col] if 'Cash Cash Equivalents And Short Term Investments' in bs.index else 0
    equity = bs.loc['Stockholders Equity', col] if 'Stockholders Equity' in bs.index else 0
    assets = bs.loc['Total Assets', col] if 'Total Assets' in bs.index else 0
    liab = bs.loc['Total Liabilities Net Minority Interest', col] if 'Total Liabilities Net Minority Interest' in bs.index else 0
    dt_str = col.strftime('%Y-%m-%d')
    print(f"=== 最新資產負債狀況 ({dt_str}) ===")
    print(f"  總資產: {assets/1e8:.2f} 億")
    print(f"  總負債: {liab/1e8:.2f} 億 (負債比率: {liab/assets*100:.2f}%)")
    print(f"  股東權益(淨值): {equity/1e8:.2f} 億")
    print(f"  每股淨值約: {equity / 136263590:.2f} 元")
    print(f"  現金及約當現金: {cash/1e8:.2f} 億")

cf = t.quarterly_cash_flow
if not cf.empty:
    col = cf.columns[0]
    ocf = cf.loc['Operating Cash Flow', col] if 'Operating Cash Flow' in cf.index else 0
    capex = cf.loc['Capital Expenditure', col] if 'Capital Expenditure' in cf.index else 0
    dt_str = col.strftime('%Y-%m-%d')
    print(f"\n=== 現金流量表狀況 ({dt_str}) ===")
    print(f"  營業現金流: {ocf/1e8:.2f} 億")
    print(f"  資本支出: {capex/1e8:.2f} 億")
    print(f"  自由現金流: {(ocf + capex)/1e8:.2f} 億")
