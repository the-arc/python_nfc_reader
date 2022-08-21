import csv
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import i2clcda as lcd
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import buzzer
from time import sleep
from datetime import datetime


csv_name = './data.csv'
raspi_name = ''
text1 = ''
text2 = ''

# GoogleCloudの認証キー
KEY_NAME = './cert/google_auth2.json' 
# GoogleSheetsのID
GOOGLE_SHEET_ID = 'XXXXX'
try:
  if __name__ == '__main__':
    # 認証処理: 
    ## アクセス権限の対象スコープをスプレッドシートとドライブに設定
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'] 
    ## アクセス権限を取得
    credentials = service_account.Credentials.from_service_account_file(filename=KEY_NAME, scopes=scope)
    ## 取得したアクセス権限でGoogleSheetsを認証
    gc = gspread.authorize(credentials)
except KeyboardInterrupt:
    pass

# 起動用
def start():
  try:
    # nfc情報を元にuser情報取得
    user = get_user(nfc_read())
    #nfcが登録されておらず、ユーザが取れなかった場合
    if user is None:
      display_view('Not Found!')
    else:
      #音声モジュールから出力
      buzzer.sound()
      # user情報と日付情報をSDとスプレッドシートに書き込み
      # 現在日時を取得(yyyy/mm/dd HH:MM:SS)
      write(user, datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
  except:
    display_view('System error...')

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
def get_raspi_name():
  global raspi_name
  serial = getserial()
  name = ''
  # スプレッドシート操作処理(マスタレコード[Sheet2]): 
  ## シートを取得
  wks3 = gc.open_by_key(GOOGLE_SHEET_ID).get_worksheet(2)
  ## シートを配列に格納
  master_records = wks3.get_all_values() 
  ## NFCカードのIDからユーザ名を取得して変数に格納
  for i in range(0, len(master_records)):
    if master_records[i][0]  == serial:
      name = master_records[i][1]
      break
  raspi_name = name
  print(raspi_name)

# idmからuser配列取得
def get_user(idm):
  display_view('wait next touch')
  user = None
  # スプレッドシート操作処理(マスタレコード[Sheet2]): 
  ## シートを取得
  wks2 = gc.open_by_key(GOOGLE_SHEET_ID).get_worksheet(1)
  ## シートを配列に格納
  master_records = wks2.get_all_values() 
  ## NFCカードのIDからユーザ名を取得して変数に格納
  for i in range(0, len(master_records)):
    if master_records[i][1]  == idm:
      user = master_records[i]
      break
  return user

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
  words = [date, getserial(), raspi_name]
  for i in range(2, len(user)):
    words.append(user[i])
  
  csv_write(words)
  spreadsheet_write(words)

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
  return cpuserial

##########################
# スプレッドシートへ書き込み
def spreadsheet_write(words):
  # スプレッドシート操作処理(トランレコード[Sheet1]): 
  ## シートを取得
  wks1 = gc.open_by_key(GOOGLE_SHEET_ID).get_worksheet(0)
  ## シートを配列に格納
  records = wks1.get_all_values()
  ## シート内に 現在の日付 と raspiのシリアル番号, NFCカードから取得したユーザ名 を記録
  for i in range(0, len(words)):
    wks1.update_cell(len(records)+1, i+1, words[i])

# csvへ書き込み
def csv_write(words):
  with open(csv_name, 'a') as f:
    writer = csv.writer(f)
    writer.writerow([words])

lcd.lcd_init()
display_view('starting...')
get_raspi_name()
while True:
  lcd.lcd_init()
  display_view('Touch the card!')
  start()
  initialization()

