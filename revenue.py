import sys
import os
import csv
import settings
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
 
  #時刻ごとにファイル名生成する場合の処理
  #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  #filename = f"output/{timestamp}.csv"

  #ファイル名を固定とする場合の処理
  filename = "output/output.csv"

  #新規書き込みw,追記モードaで使い分け
  with open(filename, mode="a", newline="", encoding="utf-8") as f:
    write = csv.DictWriter(f, fieldnames=data.keys())
    #見出し行を付ける処理
    if os.path.getsize(filename) == 0:
      write.writeheader()
    #現在ファイル名を固定としているため、csvのカラムを記述する処理はコメントアウト
    #write.writeheader()
    write.writerow(data)
  print(f"CSV出力完了:{filename}")
  return

#csvファイル読み込み関数
def input_csv(filepath):
  with open(filepath,encoding="utf-8") as f:
    reader = csv.DictReader(f)
    
    #見出し行がない場合の処理
    #reader = csv.DictReader(f, fieldnames=['商品名', '価格', '原価', '送料'])
    data = list(reader)
  
  #TODO: デバッグ用。CSV処理安定後に削除
  print(data[1])
  print(data[1]['商品名'])
  return data

def revenue(name, price, cost_price, shipping,fee_rate):
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
    "商品名": name,
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
  
  return

def main():
  #コマンドラインの引数を取得(配列の0番目は実行ファイル名になる)
  args = sys.argv

  #手数料の設定(settings.pyからfee_rateの値を取得)
  fee_rate =  settings.fee_rate
  try:
    if len(args) == 2:
      #1つ目の引数にファイル名があるならそのファイルを読み込んで実行
      input_data = input_csv(args[1]) 
      for i in input_data:
      #関数実装したものを実行
        revenue(i['商品名'],int(i['価格']), int(i['原価']),int(i['送料']),fee_rate)
      
  #引数にファイル名がない場合、inputで入力処理をさせる
    else:
      print("売買情報の入力を行ってください。")
      name = input("売買予定の商品名を入力してください。(name)>>")
      price = int(input("売買予定の商品の価格を入力してください。(price)＞>"))
      cost_price = int(input("購入予定の商品の価格を入力してください。(cost_price)＞>"))
      shipping = int(input("購入予定の商品の送料を入力してください。(shipping)＞>"))
      #関数実装したものを実行
      revenue(name ,price, cost_price,shipping,fee_rate)

  except ValueError:
    print("入力値が違います。")
    return

main()