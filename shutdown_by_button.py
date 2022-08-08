#!/usr/bin/env python

import RPi.GPIO as GPIO
import os, time

GPIO.setmode(GPIO.BCM)  # BCM番号で指定することを宣言。

# GPIO4 : shutdown button
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP) # GPIO4は入力(IN)でpull-up(PDP_UP)

def shutdown(channel):
  os.system("sudo shutdown -h now") # shutdownのshellコマンドを持つ関数の定義

GPIO.add_event_detect(4, GPIO.FALLING, callback = shutdown, bouncetime = 2000)
# ↑GPIO4が2秒(2000ms)以上"0"ならば、shutdown関数を呼ぶ

while 1:
  time.sleep(100) # GPIO4の監視は100ms間隔で行う