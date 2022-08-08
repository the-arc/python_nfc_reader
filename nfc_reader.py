import csv
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import i2clcda as lcd
from time import sleep
from datetime import datetime

csv_name = './data.csv'
text1 = ''
text2 = ''

def start():
  # nfc情報を元にuser情報取得
  user_data = get_user(nfc_read())
  # user情報と日付情報をSDとスプレッドシートに書き込み
  write(user_data.name, user_data.team, get_date())

# NFC読み込み idm取得
def nfc_read():
  reader = SimpleMFRC522()
  try:
    print('Touch the card!')
    display_view('Touch the card!')
    id, text = reader.read()
    print(id)
    display_view(str(id))
    print(text)
    print('done.')
    display_view('done.')
  finally:
      GPIO.cleanup()
  return id

# idmからuser取得
def get_user(idm):
  return

# 現在日時を取得(yyyy/mm/dd HH:MM:SS)
def get_date():
  return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def display_view(t):
  global text1
  global text2
  text1 = text2
  text2 = t
  lcd.lcd_string(text1, lcd.LCD_LINE_1)
  lcd.lcd_string(text2, lcd.LCD_LINE_2)

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
  with open(csv_name, 'a') as f:
    writer = csv.writer(f)
    writer.writerow([words])

#nfc読み込み, csv書き込みテスト
lcd.lcd_init()
csv_write(nfc_read(), 'red', get_date())