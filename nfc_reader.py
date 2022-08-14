import csv
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import i2clcda as lcd
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import time
from time import sleep
from datetime import datetime

csv_name = './data.csv'
text1 = ''
text2 = ''

# 起動用
def start():
  # nfc情報を元にuser情報取得
  user = get_user(nfc_read())
  # user情報と日付情報をSDとスプレッドシートに書き込み
  display_view('wait next touch')
  write(user, get_date())

# 状態を初期化
def initialization():
  global text1
  global text2
  text1 = ''
  text2 = ''

# NFC読み込み idm取得
def nfc_read():
  reader = SimpleMFRC522()
  try:
    id, text = reader.read()
    display_view(str(id))
    display_view('complete!')
  finally:
      GPIO.cleanup()
  return str(id)

# idmからuser配列取得
def get_user(idm):
  # スプレッドシート操作処理(マスタレコード): 
  ## シートを取得
  wks2 = gc.open_by_key(GOOGLE_SHEET_ID).get_worksheet(1)
  ## シートを配列に格納
  master_records = wks2.get_all_values() 
  ## NFCカードのIDからユーザ名を取得して変数に格納
  for i in range(0, len(master_records)):
    if master_records[i][0]  == idm:
      user = master_records[i]
      break
  return user

# 現在日時を取得(yyyy/mm/dd HH:MM:SS)
def get_date():
  return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

# ディスプレイ表示用
def display_view(t):
  global text1
  global text2
  text1 = text2
  text2 = t
  lcd.lcd_string(text1, lcd.LCD_LINE_1)
  lcd.lcd_string(text2, lcd.LCD_LINE_2)

# csv,スプレッドシート書き込み
def write(user, date):
  csv_write(user, date)
  spreadsheet_write(user, date)

##########################
# スプレッドシートへ書き込み write関数から呼び出し
def spreadsheet_write(user, date):
  # スプレッドシート操作処理(トランレコード): 
  ## シートを取得
  wks1 = gc.open_by_key(GOOGLE_SHEET_ID).get_worksheet(0)
  ## シートを配列に格納
  records = wks1.get_all_values()
  ## シート内に 現在の日付 と NFCカードから取得したユーザ名 を記録
  wks1.update_cell(len(records)+1, 1, date)
  wks1.update_cell(len(records)+1, 2, user[1])
  wks1.update_cell(len(records)+1, 3, user[2])

# csvへ書き込み(user, team, date) write関数から呼び出し
def csv_write(user, date):
  words = [user[1], user[2], date]
  with open(csv_name, 'a') as f:
    writer = csv.writer(f)
    writer.writerow([words])

lcd.lcd_init()
while True:
  display_view('Touch the card!')
  start()
  initialization()

