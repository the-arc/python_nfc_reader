import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import i2clcda as lcd
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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

# ディスプレイ表示用
def display_view(t):
  global text1
  global text2
  text1 = text2
  text2 = t
  lcd.lcd_string(text1, lcd.LCD_LINE_1)
  lcd.lcd_string(text2, lcd.LCD_LINE_2)

# NFC読み込み idm取得
def nfc_read():
  reader = SimpleMFRC522()
  try:
    id, text = reader.read()
    display_view(str(id))
  finally:
      GPIO.cleanup()
  return str(id)

# スプレッドシートへ書き込み write関数から呼び出し
def spreadsheet_write(idm):
  # スプレッドシート操作処理(マスタレコード): 
  ## シートを取得
  wks2 = gc.open_by_key(GOOGLE_SHEET_ID).get_worksheet(1)
  ## シートを配列に格納
  master_records = wks2.get_all_values() 
  user = None
  for i in range(0, len(master_records)):
    if master_records[i][1] == idm:
      user = master_records[i]
      display_view('already use')
  if user is None:
    ## シートを配列に格納
    records = wks2.get_all_values()
    ## シート内にidmを記録
    wks2.update_cell(len(records)+1, 1, str(len(records)))
    wks2.update_cell(len(records)+1, 2, idm)
    display_view('finished!')

lcd.lcd_init()
display_view('register mode')
while True:
  display_view('Touch the card!')
  spreadsheet_write(nfc_read())