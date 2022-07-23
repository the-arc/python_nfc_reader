import csv
from datetime import datetime

csv_name = 'data.csv'

def start():
    user_data = get_user(nfc_read())
    write(user_data.name, user_data.team, get_date())

# NFC読み込み idm取得
def nfc_read():
    return

# idmからuser取得
def get_user(idm):
    return

# 現在日時を取得(yyyy/mm/dd HH:MM:SS)
def get_date(): 
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

# csv,スプレッドシート書き込み
def write(user, team, date):
    csv_write(user, team, date)
    spreadsheet_write(user, team, date)

##########################
# スプレッドシートへ書き込み write関数から呼び出し
def spreadsheet_write(user, team, date):
    return

# csvへ書き込み(user, team, date) write関数から呼び出し
def csv_write(user, team, date):
    words = [user, team, date]
    with open (csv_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([words])