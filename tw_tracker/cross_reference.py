# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
from generate_today_format_a import DAILY_RECORDS

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

buy_tracker = defaultdict(lambda: {'count': 0, 'brokers': [], 'total_amount': 0, 'total_shares': 0, 'price': 0, 'name': ''})
sell_tracker = defaultdict(lambda: {'count': 0, 'brokers': [], 'total_amount': 0, 'total_shares': 0, 'price': 0, 'name': ''})

for broker, records in DAILY_RECORDS.items():
    buyers = [r for r in records if r['net_shares'] > 0]
    buyers.sort(key=lambda x: x['net_shares'] * x['price'], reverse=True)
    for b in buyers[:10]:
        code = b['stock_code']
        amt = b['net_shares'] * 1000 * b['price']
        buy_tracker[code]['count'] += 1
        buy_tracker[code]['brokers'].append(broker)
        buy_tracker[code]['total_amount'] += amt
        buy_tracker[code]['total_shares'] += b['net_shares']
        buy_tracker[code]['price'] = b['price']
        buy_tracker[code]['name'] = b['stock_name']

    sellers = [r for r in records if r['net_shares'] < 0]
    sellers.sort(key=lambda x: abs(x['net_shares'] * x['price']), reverse=True)
    for s in sellers[:10]:
        code = s['stock_code']
        amt = abs(s['net_shares'] * 1000 * s['price'])
        sell_tracker[code]['count'] += 1
        sell_tracker[code]['brokers'].append(broker)
        sell_tracker[code]['total_amount'] += amt
        sell_tracker[code]['total_shares'] += abs(s['net_shares'])
        sell_tracker[code]['price'] = s['price']
        sell_tracker[code]['name'] = s['stock_name']

print("=== 多方主力共識榜 (BUY CONSENSUS) ===")
for code, data in sorted(buy_tracker.items(), key=lambda x: (x[1]['count'], x[1]['total_amount']), reverse=True):
    b_names = "、".join(data['brokers'])
    print(f"{data['name']} ({code}) | 共識分點數: {data['count']}/11 | 總買超金額: +{data['total_amount']/1e8:.2f} 億 | 淨買超: {data['total_shares']:,} 張 | 進駐分點: {b_names}")

print("\n=== 空方主力調節共識榜 (SELL CONSENSUS) ===")
for code, data in sorted(sell_tracker.items(), key=lambda x: (x[1]['count'], x[1]['total_amount']), reverse=True):
    b_names = "、".join(data['brokers'])
    print(f"{data['name']} ({code}) | 調節分點數: {data['count']}/11 | 總賣超金額: -{data['total_amount']/1e8:.2f} 億 | 淨賣超: {data['total_shares']:,} 張 | 調節分點: {b_names}")

clashes = set(buy_tracker.keys()) & set(sell_tracker.keys())
print("\n=== 多空對作 / 籌碼分歧衝突榜 (TUG OF WAR) ===")
if not clashes:
    print("今日 11 大主力多空共識極度高度一致，無重大對作分歧標的！")
else:
    for code in clashes:
        print(f"{code} 買超 {buy_tracker[code]['count']} 家 vs 賣超 {sell_tracker[code]['count']} 家")
