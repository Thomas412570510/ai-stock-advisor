# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request, ssl, csv, io

ctx = ssl._create_unverified_context()
url = 'https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    content = resp.read().decode('utf-8')
    reader = csv.reader(io.StringIO(content))
    header = next(reader)
    
    levels_map = {
        '1': '1~999 股 (零股散戶)',
        '2': '1~5 張 (小資散戶)',
        '3': '5~10 張',
        '4': '10~15 張',
        '5': '15~20 張',
        '6': '20~30 張',
        '7': '30~40 張',
        '8': '40~50 張 (50張以下散戶分界)',
        '9': '50~100 張 (中實戶)',
        '10': '100~200 張',
        '11': '200~400 張',
        '12': '400~600 張 (大戶)',
        '13': '600~800 張 (大戶)',
        '14': '800~1,000 張 (大戶)',
        '15': '1,000 張以上 (千張超大戶)'
    }
    
    rows = []
    for r in reader:
        if len(r) >= 6 and r[1].strip() == '5234':
            rows.append(r)
            
    print(f"找到 5234 資料筆數: {len(rows)}")
    if rows:
        print("最新資料日期:", rows[0][0])
        print("-" * 65)
        print(f"{'級距名稱':<25} | {'人數':>8} | {'總股數 (張)':>12} | {'佔比 (%)':>8}")
        print("-" * 65)
        
        retail_under_10_shares = 0
        retail_under_10_people = 0
        retail_under_10_pct = 0.0
        
        retail_under_50_shares = 0
        retail_under_50_people = 0
        retail_under_50_pct = 0.0
        
        for r in rows:
            lvl = r[2].strip()
            name = levels_map.get(lvl, f"等級 {lvl}")
            people = int(r[3])
            shares = int(r[4])
            pct = float(r[5])
            print(f"{name:<25} | {people:8,d} | {shares/1000:10,.1f} 張 | {pct:7.2f}%")
            
            # 統計小散戶 (10張以下: 等級 1~3)
            if lvl in ['1', '2', '3']:
                retail_under_10_shares += shares
                retail_under_10_people += people
                retail_under_10_pct += pct
                
            # 統計全體一般散戶 (50張以下: 等級 1~8)
            if int(lvl) <= 8:
                retail_under_50_shares += shares
                retail_under_50_people += people
                retail_under_50_pct += pct

        print("=" * 65)
        print(f"👉 【極小資散戶 (10張以下)】: 共 {retail_under_10_people:,} 人 | 持有 {retail_under_10_shares/1000:,.1f} 張 | 佔比: {retail_under_10_pct:.2f}%")
        print(f"👉 【全體一般散戶 (50張以下)】: 共 {retail_under_50_people:,} 人 | 持有 {retail_under_50_shares/1000:,.1f} 張 | 佔比: {retail_under_50_pct:.2f}%")
