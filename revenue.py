import sys

########################################################################
#メルカリ出品前に利益と利益率を計算するツール
#使い方;
#コマンドラインにpython revenue.py 売値(数値) 原価(数値) 送料(数値)
#例python revenue.py 5000 3000 500
########################################################################

def calc_profit(price,cost_price, shipping, fee_rate):
  return price - cost_price - shipping - ( price * fee_rate)

def main():
  #コマンドラインの引数を取得(配列の0番目は実行ファイル名になる)
  args = sys.argv
  fee_rate = 0.1

  if len(args) == 4:
    try:
      price = int(args[1])
      cost_price = int(args[2])
      shipping = int(args[3])
      profit = int(calc_profit(price, cost_price, shipping, fee_rate))

      print("価格:", price)
      print("原価:", cost_price)
      print("送料:", shipping)
      print("手数料:", int(price * fee_rate))
      print("利益:", profit)
      if cost_price  == 0:
        print("利益率(原価基準):", int(profit / cost_price * 100),"%")
      else:
        print("利益率(原価基準):計算不可")
      print("利益率(売価基準):", int(profit / price * 100),"%")
      if profit < 0:
        print("赤字です")
      elif profit < 300:
        print("利益が少なめです。(要塞検討)")
      else:
        print("出品候補です")

    except ValueError:
      print("数値を入力してください")
      return

  else:
    print("引数が不正です。")
    print("例 python revenue.py 3000 2000 750")

main()