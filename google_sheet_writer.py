# -*- coding: utf-8 -*-
"""
# ラズパイNFCリーダ / ログ記録サービス テストプログラム
- google.oauth2認証
- Googleスプレッドへの読み込み・書き込み

# 実行環境
- 言語: Python 3.9.2

# 必須パッケージ
- sudo pip3 install gspread
- sudo pip3 install google-api-python-client

# LINK
- [ラズパイからPyhtonでGoogleスプレッドシートやドライブにアクセスする方法](https://www.souichi.club/raspberrypi/google-oauth2/)
- [test_sheet](******)
"""

import gspread
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# GoogleCloudの認証キー
KEY_NAME = './cert/******.json' 
# GoogleSheetsのID
GOOGLE_SHEET_ID = '******' 
# NFCカードのID
NFC_ID = '1'
# NFCカードから取得したユーザ名
NAME = 'unknown'

try:
    if __name__ == '__main__':

        # 認証処理: 
        ## アクセス権限の対象スコープをスプレッドシートとドライブに設定
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'] 
        ## アクセス権限を取得
        credentials = service_account.Credentials.from_service_account_file(filename=KEY_NAME, scopes=scope)
        ## 取得したアクセス権限でGoogleSheetsを認証
        gc = gspread.authorize(credentials)

        # スプレッドシート操作処理(マスタレコード): 
        ## シートを取得
        wks2 = gc.open_by_key(GOOGLE_SHEET_ID).get_worksheet(1) 
        ## シートを配列に格納
        master_records = wks2.get_all_values() 
        ## NFCカードのIDからユーザ名を取得して変数に格納
        for i in range(0, len(master_records)):
            if master_records[i][0]  == NFC_ID:
                NAME = master_records[i][1]
                break;

        # スプレッドシート操作処理(トランレコード): 
        ## シートを取得
        wks1 = gc.open_by_key(GOOGLE_SHEET_ID).get_worksheet(0)
        ## シートを配列に格納
        records = wks1.get_all_values()
        ## 現在の日付を格納
        dt_now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') 
        ## シート内に 現在の日付 と NFCカードから取得したユーザ名 を記録
        wks1.update_cell(len(records)+1, 1, dt_now)
        wks1.update_cell(len(records)+1, 2, NAME)

except KeyboardInterrupt:
    pass
