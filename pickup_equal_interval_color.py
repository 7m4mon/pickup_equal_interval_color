# coding: utf-8

'''
LEDギャラリー[https://w.atwiki.jp/led-gallery/]
の画像を保存したフォルダに対して一括でサイズの縮小＆減色するプログラム。
3 ピクセル毎にピックアップして、予め設定したパレットから近似色を選ぶ。
減色方法はパレットからのピックアップか、計算が選べるようになっています。
パレットは [led-gallery(R,G,B), led-matrix(R,G,B)]の順になっていて
ピックアップした色を最も近い色[0]に対応する色[1]に置き換えます。
計算する場合、1/4 scan (64ずつ) で切り捨てた値にします。
実際に Pico LED Matrix で表示させるには JTrimによる後処理（256色化）が必要です。

2023.3 7M4MON
'''

from PIL import Image
import math
import glob
from pathlib import Path


SUB_DIR = 'enoden-1000'
REDUCE_COLOR_METHOD = 'CALC' # 'CALC' or 'PALETTE'
LED_COLOR_TYPE = 'FULL'      # 'ORANGE' or 'FULL'

# color_palette [[led-gallery(R,G,B), led-matrix(R,G,B)], ... ]

if LED_COLOR_TYPE == 'ORANGE':
    color_palette = [                   # 3 Color LED
        [(51,51,51),(0,0,0)],           # Black
        [(255,0,0),(255,0,0)],          # Red
        [(0,255,0),(0,255,0)],          # Green
        [(255,153,51),(255,127,0)]      # Orange
        ] 
else:
    color_palette = [                   # Full Color LED
        [(51,51,51),(0,0,0)],           # Black
        [(142,142,142),(127,127,127)],  # White
        [(255,255,255),(255,255,255)],  # White
        [(255,0,0),(255,0,0)],          # Red
        [(0,255,0),(0,255,0)],          # Lime
        [(0,0,255),(0,0,255)],          # Blue
        [(0,153,0),(0,127,0)],          # Green (通勤準急)
        [(0,147,103),(0,127,0)],        # Green (東京経由)
        [(255,127,39),(255,127,0)],     # Orange
        [(183,74,255),(127,0,255)],     # Purple（通勤快速）
        [(21,173,255),(0,127,255)],     # Cyan（特別快速）
        [(253,43,116),(255,0,127)],     # Pink（快速)
        [(0,183,147),(0,127,127)],      # Aqua（準急)
        [(255,102,204),(255,63,255)],   # Pink2
        [(0,166,129),(0,127,127)],      # Aqua
        [(255,255,0),(255,255,0)]       # Yellow
        ] 

def round_quoter_scan(num):
    num += 1
    num = math.floor(num/64)
    num *= 64
    if num != 0:
        num -= 1
    return num

def calc_approximate_color(c):
    rc = [0,0,0]
    for i in range(3):
        rc[i] = round_quoter_scan(c[i])
    rt = (rc[0], rc[1], rc[2])
    return rt


def get_approximate_color(c):
    min_distance = 99999
    index = 0
    color_index = 0
    for cp in color_palette:
        distance = math.sqrt( (cp[0][0]-c[0])*(cp[0][0]-c[0])+(cp[0][1]-c[1])*(cp[0][1]-c[1])+(cp[0][2]-c[2])*(cp[0][2]-c[2])) 
        if distance < min_distance:
            min_distance = distance
            color_index = index
        index += 1
    return color_palette[color_index][1]


def convert_approximate_color(file_name):
    im = Image.open(file_name)  # 画像を開く
    im = im.convert('RGB')

    start_x = 2
    start_y = 2
    step_pix = 3

    pic_width = int(math.floor((im.width - start_x ) / step_pix) + 1)
    pic_height = int(math.floor((im.height - start_y) / step_pix) + 1)

    pic = Image.new('RGB', (pic_width, pic_height) )

    print(str(pic_width) + ' x ' + str(pic_height))

    for x in range(pic_width):
        for y in range(pic_height):
            pix_color = im.getpixel((start_x + x*step_pix, start_y + y*step_pix))
            if REDUCE_COLOR_METHOD == 'CALC':
                pic.putpixel((x,y),calc_approximate_color(pix_color))
            else:            
                pic.putpixel((x,y),get_approximate_color(pix_color))

    #pic.show()
    pic.save( file_name + '_.bmp', 'bmp')

def main():
    files = glob.glob("./" + SUB_DIR + "/*.png")
    for file in files:
        print(file)
        convert_approximate_color(file)

if __name__ == '__main__':
    main()
