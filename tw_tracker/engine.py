# -*- coding: utf-8 -*-
"""
tw_broker_tracker_engine.py
落實 tw-broker-tracker 雙快捷指令 (高質感雙向對照排版版)：
  - Format A: 當日榜 (買賣超左右並排對照表格，依金額 TOP 10 排序)
  - Format B: 當週榜 (買賣超左右並排對照表格，依近 7 日天數 TOP 10 排序)
"""

import sys
from typing import List, Dict, Any
import pandas as pd

# Windows CP950 Unicode 相容性處理 (防止 emoji 導致編碼崩潰)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 11 大核心追蹤主力分點
CORE_BROKERS = [
    "國票-敦北法人",
    "凱基-城中",
    "統一-城中",
    "國票-安和",
    "元大證券",
    "富邦證券",
    "統一證券",
    "群益金鼎",
    "美商高盛",
    "美林證券",
    "摩根大通"
]

def format_amount(amount_in_ntd: float) -> str:
    """金額自動格式化為高對比標籤格式 (+X.XX 億 / -X.XX 億 / +X,XXX 萬)"""
    amt = abs(amount_in_ntd)
    sign = "+" if amount_in_ntd > 0 else ("-" if amount_in_ntd < 0 else "")
    if amt >= 100_000_000:
        return f"{sign}{amt / 100_000_000:.2f} 億"
    else:
        return f"{sign}{amt / 10_000:,.0f} 萬"


# =====================================================================
# 1️⃣ Format A: 當日榜 (高質感雙向對照表格)
# =====================================================================
def generate_format_a_daily(broker_daily_records: Dict[str, List[Dict[str, Any]]], date_str: str) -> str:
    """
    產生「當日」標準高質感雙向對照表格 (Format A)
    左側買超 TOP 10 ｜ 右側賣超 TOP 10 一覽無遺
    """
    output = []
    output.append(f"## 📊 【Format A：當日 11 大主力分點買賣超明細榜 ({date_str})】\n")

    for broker_name in CORE_BROKERS:
        records = broker_daily_records.get(broker_name, [])
        if not records:
            continue

        # 計算淨額 (元) = 淨張數 * 1000 * 均價
        for r in records:
            r['net_amount'] = r['net_shares'] * 1000 * r['price']

        # 買超依金額由大到小排序 TOP 10
        buyers = [r for r in records if r['net_shares'] > 0]
        buyers.sort(key=lambda x: x['net_amount'], reverse=True)

        # 賣超依金額絕對值由大到小排序 TOP 10
        sellers = [r for r in records if r['net_shares'] < 0]
        sellers.sort(key=lambda x: abs(x['net_amount']), reverse=True)

        # 生成核心摘要提示卡
        b1_str = f"**{buyers[0]['stock_name']}** (`{format_amount(buyers[0]['net_amount'])}`)" if len(buyers) > 0 else "無"
        b2_str = f"、**{buyers[1]['stock_name']}** (`{format_amount(buyers[1]['net_amount'])}`)" if len(buyers) > 1 else ""
        s1_str = f"**{sellers[0]['stock_name']}** (`{format_amount(sellers[0]['net_amount'])}`)" if len(sellers) > 0 else "無"

        output.append(f"### 🏢 【{broker_name}】")
        output.append(f"> 💡 **核心動態**：多方加碼 {b1_str}{b2_str} ｜ 空方調節 {s1_str}\n")
        
        # 雙向對照表格頭部
        output.append("| 榜位 | 💰 買超標的 (代號) | 淨買金額 | 淨買張數 @ 均價 | 🔴 賣超標的 (代號) | 淨賣金額 | 淨賣張數 @ 均價 |")
        output.append("| :---: | :--- | :---: | :--- | :--- | :---: | :--- |")

        # 10 檔不截斷完整輸出
        for rank in range(1, 11):
            rank_idx = rank - 1
            
            # 買超欄位
            if rank_idx < len(buyers):
                b = buyers[rank_idx]
                b_amt = format_amount(b['net_amount'])
                b_col_stock = f"**{b['stock_name']}** `{b['stock_code']}`"
                b_col_amt = f"`{b_amt}`"
                b_col_detail = f"{int(b['net_shares']):,} 張 @ {b['price']:.1f} 元"
            else:
                b_col_stock, b_col_amt, b_col_detail = "—", "—", "—"

            # 賣超欄位
            if rank_idx < len(sellers):
                s = sellers[rank_idx]
                s_amt = format_amount(s['net_amount'])
                s_col_stock = f"**{s['stock_name']}** `{s['stock_code']}`"
                s_col_amt = f"`{s_amt}`"
                s_col_detail = f"{abs(int(s['net_shares'])):,} 張 @ {s['price']:.1f} 元"
            else:
                s_col_stock, s_col_amt, s_col_detail = "—", "—", "—"

            output.append(
                f"| **{rank:02d}** | {b_col_stock} | {b_col_amt} | {b_col_detail} | {s_col_stock} | {s_col_amt} | {s_col_detail} |"
            )
            
        output.append("\n---\n")

    return "\n".join(output)


# =====================================================================
# 2️⃣ Format B: 當週榜 (高質感波段對照表格)
# =====================================================================
def generate_format_b_weekly(broker_multi_day_records: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    產生「當週」標準高質感雙向對照表格 (Format B)
    左側買超天數最多 TOP 10 ｜ 右側賣超天數最多 TOP 10
    """
    output = []
    output.append("## 🗓️ 【Format B：當週 11 大主力分點週波段買賣超榜（近 7 日天數排序）】\n")

    for broker_name in CORE_BROKERS:
        records = broker_multi_day_records.get(broker_name, [])
        if not records:
            continue

        buyers = [r for r in records if r.get('buy_days_in_7d', 0) > 0]
        buyers.sort(key=lambda x: (x['buy_days_in_7d'], x.get('net_amount_5d', 0)), reverse=True)

        sellers = [r for r in records if r.get('sell_days_in_7d', 0) > 0]
        sellers.sort(key=lambda x: (x['sell_days_in_7d'], abs(x.get('net_amount_5d', 0))), reverse=True)

        output.append(f"### 🏢 【{broker_name}】 (近 7 日波段籌碼)")
        output.append("| 榜位 | 💰 買超標的 (代號) | 買超天數 | 5日淨買超 (今日) | 🔴 賣超標的 (代號) | 賣超天數 | 5日淨賣超 (今日) |")
        output.append("| :---: | :--- | :---: | :--- | :--- | :---: | :--- |")

        for rank in range(1, 11):
            rank_idx = rank - 1

            if rank_idx < len(buyers):
                b = buyers[rank_idx]
                b_5d = format_amount(b.get('net_amount_5d', 0))
                b_today = format_amount(b.get('today_amount', 0))
                b_stock = f"**{b['stock_name']}** `{b['stock_code']}`"
                b_days = f"**{b['buy_days_in_7d']} 天**"
                b_val = f"`{b_5d}` (`{b_today}`)"
            else:
                b_stock, b_days, b_val = "—", "—", "—"

            if rank_idx < len(sellers):
                s = sellers[rank_idx]
                s_5d = format_amount(s.get('net_amount_5d', 0))
                s_today = format_amount(s.get('today_amount', 0))
                s_stock = f"**{s['stock_name']}** `{s['stock_code']}`"
                s_days = f"**{s['sell_days_in_7d']} 天**"
                s_val = f"`{s_5d}` (`{s_today}`)"
            else:
                s_stock, s_days, s_val = "—", "—", "—"

            output.append(
                f"| **{rank:02d}** | {b_stock} | {b_days} | {b_val} | {s_stock} | {s_days} | {s_val} |"
            )

        output.append("\n---\n")

    return "\n".join(output)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "當日"
    from generate_today_format_a import DAILY_RECORDS
    
    if mode in ["當日", "單日", "單日榜"]:
        print(generate_format_a_daily(DAILY_RECORDS, "2026-09-21"))
    else:
        print("請指定模式")
