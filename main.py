from pycoingecko import CoinGeckoAPI
import pandas as pd
import sqlite3
from decimal import Decimal
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
import numpy as np
import os


#  抽出カラムlist['symbol', 'name', 'current_price', 'market_cap_rank', 'price_change_percentage_1h_in_currency', 'price_change_percentage_24h_in_currency', 'price_change_percentage_7d_in_currency']

# ids='bitcoin, ripple, ethereum, polkadot, bitcoin-cash,
# nem, factom, lisk, litecoin, ethereum-classic,
# stellar-lumens, monacoin, qtum, basic-attention-token, iost,
# enjin-coin, omg-network, plateau-finance, tezos, enjin-coin,
# cosmos, symbol, qash, tron, cardano,
# huobi-token, ontology, jasmycoin, chainlink',

# init
def init(protfolio_db_name, market_data):
    portfolio_db = Db(protfolio_db_name)
    portfolio_db.db_create()
 # 保有コインの設定、未保有のコインの設定 サンプル
    data = ('btc', '0.00004712', '5545937')
    portfolio_db.db_insert(data)
    data = ('eth', '0.0006336', '468253')
    portfolio_db.db_insert(data)
    data = ('xrp', '2.814285', '94.15')
    portfolio_db.db_insert(data)
    data = ('dot', '0.0', str(market_data.at['dot', 'current_price']))
    portfolio_db.db_insert(data)
    data = ('ltc', '0.0', str(market_data.at['ltc', 'current_price']))
    portfolio_db.db_insert(data)
    data = ('link', '0.0', str(market_data.at['link', 'current_price']))
    portfolio_db.db_insert(data)
    data = ('bch', '0.0', str(market_data.at['bch', 'current_price']))
    portfolio_db.db_insert(data)
    data = ('etc', '0.0', str(market_data.at['etc', 'current_price']))
    portfolio_db.db_insert(data)
    data = ('xtz', '0.0', str(market_data.at['xtz', 'current_price']))
    portfolio_db.db_insert(data)
    data = ('bat', '2.45386739', '126')
    portfolio_db.db_insert(data)
    data = ('xem', '0.0', str(market_data.at['xem', 'current_price']))
    portfolio_db.db_insert(data)
    data = ('lsk', '0.0', str(market_data.at['lsk', 'current_price']))
    portfolio_db.db_insert(data)
    data = ('mona', '1.69551489', '172')
    portfolio_db.db_insert(data)

    return portfolio_db


def get_marketsdata():
    cg = CoinGeckoAPI()
    r = cg.get_coins_markets(vs_currency='jpy',
                             ids='bitcoin, ripple, ethereum, polkadot, tezos, stellar-lumens, nem, basic-attention-token, ethereum-classic, litecoin, bitcoin-cash, monacoin, lisk, chainlink',
                             # category='',
                             order='market_cap_desc',
                             per_page=100,
                             page=1,
                             sparkline=False,
                             price_change_percentage='1h,24h,7d'
                             )
    r2 = pd.DataFrame(r)

    return r2


def get_price(r):
    #  抽出カラムlist index: 'symbol' ['name', 'current_price', 'market_cap_rank', 'price_change_percentage_1h_in_currency', 'price_change_percentage_24h_in_currency', 'price_change_percentage_7d_in_currency']
    price_list = r[['symbol', 'name', 'current_price', 'market_cap_rank', 'price_change_percentage_1h_in_currency',
                    'price_change_percentage_24h_in_currency', 'price_change_percentage_7d_in_currency']]
    df = price_list.set_index('symbol')

    return df


# データベースの操作
class Db():
    def __init__(self, dbname):
        self.db = dbname

    def db_create(self):
        # 値をデータベースに格納
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        create_table = '''CREATE TABLE IF NOT EXISTS portfolio (coin text, amount text, buy_price text)'''
        c.executescript(create_table)
        # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
        # タプルで渡す．
        conn.commit()
        c.close()
        conn.close()

    def db_insert(self, entity):
        # 値をデータベースに格納
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = 'insert into portfolio (coin, amount, buy_price) values (?,?,?)'
        c.execute(sql, entity)
        conn.commit()
        c.close()
        conn.close()

    def db_update(self, entity):
        # 値をデータベースに格納
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        # executeメソッドでSQL文を実行する
        sql = '''update portfolio set amount = ?, buy_price = ? where coin = ?'''
        c.execute(sql, entity)
        conn.commit()
        c.close()
        conn.close()

    def db_delete(self, entity):
        # 値をデータベースに格納
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        sql = 'delete from portfolio where coin = ?'
        c.execute(sql, entity)
        conn.commit()
        c.close()
        conn.close()

    def db_output(self):
        # データベースから値を抽出
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        sql = 'select * from portfolio'
        c.execute(sql)
        match_rate = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return match_rate

    def db_one_output(self, entity):
        # データベースから値を抽出
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        sql = '''select * from portfolio where coin = ?'''
        c.execute(sql, (entity,))
        match_one = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return match_one


def remove_all():
    for record in app1.get_children():
        app1.delete(record)


def insert_item(app1, coin_model, market_data):
    i = 0
    for coin in coin_model:
        app1.insert("", "end", values=(
            coin.upper(),
            market_data.at[coin, 'name'],
            market_data.at[coin, 'market_cap_rank'],
            "{:,.2f}".format(market_data.at[coin, 'current_price']),
            "{:,.8f}".format(Decimal(db_data[i][1])),
            "{:,.8f}".format(total_new_coin[i]),
            "{:,.2f}".format(pl_per_coin[i]),
            "{:,.2f}".format(
                market_data.at[coin, 'price_change_percentage_1h_in_currency']),
            "{:,.2f}".format(
                market_data.at[coin, 'price_change_percentage_24h_in_currency']),
            "{:,.2f}".format(
                market_data.at[coin, 'price_change_percentage_7d_in_currency'])
        ))
        i = i+1


def update():
    remove_all()
    market_data = get_price(get_marketsdata())
    insert_item(app1, coin_model, market_data)


def piechart():
    plt.pie(total_new_coin, labels=market_data.index.str.upper(),
            autopct='%1.1f%%', counterclock=False, startangle=90)
    plt.axis('equal')
    plt.show()


if __name__ == "__main__":

    pl_per_coin = []
    total_pl_coin = []
    total_new_coin = []
    coin_model = []

    market_data = get_price(get_marketsdata())

    coin_model = market_data.index

    # # 新規ポートフォリオの追加
    protfolio_db_name = "protfolio.db"
    if not os.path.exists(protfolio_db_name):
        portfolio_db = init(protfolio_db_name, market_data)
        db_data = portfolio_db.db_output()
    else:
        portfolio_db = Db(protfolio_db_name)
        db_data = portfolio_db.db_output()

    i = 0
    for coin in coin_model:
        current_value = market_data.at[coin, 'current_price']
        if Decimal(db_data[i][1]) > 0:
            data = Decimal(str(current_value)) - Decimal(db_data[i][2])
        else:
            data = Decimal(str('0'))
        pl_per_coin = np.append(pl_per_coin, data)
        i = i + 1

    i = 0
    for coin in coin_model:
        data = pl_per_coin[i] * Decimal(db_data[i][1])
        total_pl_coin = np.append(total_pl_coin, data)
        i = i + 1

    i = 0
    for coin in coin_model:
        current_value = market_data.at[coin, 'current_price']
        data = Decimal(str(current_value)) * Decimal(db_data[i][1])
        total_new_coin = np.append(total_new_coin, data)
        i = i + 1

    total_pl = np.sum(total_pl_coin)

    # GUI

    # event loop
    app = tk.Tk()
    app.title("Crypto Currency Portfolio")
    app.geometry("1400x250")

    frame = ttk.Frame(app)
    frame.pack(fill=tk.BOTH, padx=10, pady=10)

    tree_scroll = ttk.Scrollbar(frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    app1 = ttk.Treeview(
        frame, yscrollcommand=tree_scroll.set, selectmode="extended")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("", "12", "bold"), )

    app1["columns"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    app1["show"] = "headings"
    app1.heading(1, text="Symbol")
    app1.heading(2, text="Name")
    app1.heading(3, text="Rank")
    app1.heading(4, text="市場価格")
    app1.heading(5, text="保 有 数")
    app1.heading(6, text="現在価格")
    app1.heading(7, text="損益/コイン")
    app1.heading(8, text="1H Change")
    app1.heading(9, text="24H Change")
    app1.heading(10, text="7D Change")

    app1.column(1, anchor=tk.CENTER, width=100)
    app1.column(2, anchor=tk.E, width=150)
    app1.column(3, anchor=tk.CENTER, width=50)
    app1.column(4, anchor=tk.E, width=150)
    app1.column(5, anchor=tk.CENTER, width=150)
    app1.column(6, anchor=tk.CENTER, width=150)
    app1.column(7, anchor=tk.CENTER, width=150)
    app1.column(8, anchor=tk.CENTER, width=150)
    app1.column(9, anchor=tk.CENTER, width=150)
    app1.column(10, anchor=tk.CENTER, width=150)

    insert_item(app1, coin_model, market_data)

    piechart_button = tk.Button(
        frame, text="Pie Chart", command=piechart)
    update_button = tk.Button(frame, text="現在価格更新", command=update)

    if total_pl > 0:
        label = tk.Label(frame, text="P/L : " +
                         "{:,.8f}".format(total_pl), foreground='green')
    else:
        label = tk.Label(frame, text="P/L : " +
                         "{:,.8f}".format(total_pl), foreground='red')

    app1.pack()
    tree_scroll.config(command=app1.yview)
    update_button.pack(side=tk.RIGHT)
    piechart_button.pack(side=tk.RIGHT)
    label.pack(side=tk.LEFT)

    app.mainloop()
