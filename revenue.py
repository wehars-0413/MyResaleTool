import sys
import os
import csv
from datetime import datetime

########################################################################
#メルカリ出品前に利益と利益率を計算するツール
#使い方;
#コマンドラインにpython revenue.py 売値(数値) 原価(数値) 送料(数値)
#例python revenue.py 5000 3000 500
########################################################################

#利益の計算を行う関数
def calc_profit(price,cost_price, shipping, fee_rate):
  return price - cost_price - shipping - ( price * fee_rate)

#csvファイルへの書き込みを行う関数
def export_result_csv(data: dict):
  #outputディレクトリがなければ作成
  os.makedirs("output", exist_ok=True)
  #ファイル名生成
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  filename = f"output/{timestamp}.csv"

  with open(filename, mode="w", newline="", encoding="utf-8") as f:
    write = csv.DictWriter(f, fieldnames=data.keys())
    write.writeheader()
    write.writerow(data)
  print(f"CSV出力完了:{filename}")
  return

def main():
  #コマンドラインの引数を取得(配列の0番目は実行ファイル名になる)
  args = sys.argv
  fee_rate = 0.1

  if len(args) == 4:
    try:
      #1つ目の引数を価格
      price = int(args[1])
      #2つ目の引数を原価
      cost_price = int(args[2])
      #3つ目の引数を送料
      shipping = int(args[3])
      #利益の計算
      profit = int(calc_profit(price, cost_price, shipping, fee_rate))
      #利益率(原価基準)
      #小数点以下を切り捨ての為int型へ
      profit_b = int(profit / cost_price * 100)
      #利益率(売価基準)
      #小数点以下を切り捨ての為int型へ
      profit_s = int(profit / price * 100)
      #判定用
      judge = "未判定"

      print("価格:", price)
      print("原価:", cost_price)
      print("送料:", shipping)
      print("手数料:", int(price * fee_rate))
      print("利益:", profit)
      if cost_price  > 0:
        print("利益率(原価基準):", profit_b,"%")
      else:
        print("利益率(原価基準):計算不可")
      print("利益率(売価基準):",  profit_s,"%")

      if profit < 0:
        judge = "赤字です"
      elif profit < 300:
        judge = "利益が少なめです。(要塞検討)"
      else:
        judge = "出品候補です"
      print("判定:",judge)

    #上記出力結果をファイルに書き込む
      data = {
        "価格": price,
        "原価": cost_price,
        "送料": shipping,
        "手数料": int(price * fee_rate),
        "利益": profit,
        "利益率(原価基準)": profit_b,
        "利益率(売価基準)": profit_s,
        "判定": judge,
        "日時": datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
      }
      #csvファイルへの書き込み
      export_result_csv(data)

    except ValueError:
      print("数値を入力してください")
      return

  else:
    print("引数が不正です。")
    print("例 python revenue.py 3000 2000 750")

main()