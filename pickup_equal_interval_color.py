# coding: utf-8

'''
LEDギャラリー[https://w.atwiki.jp/led-gallery/]
の画像を保存したフォルダに対して一括で
サイズの縮小＆減色するプログラム。
3 ピクセル毎にピックアップして、予め設定したパレットから近似色を選ぶ
実際に Pico LED Matrix で表示させるには JTrimによる後処理（256色化）が必要

2023.3 7M4MON
'''

from PIL import Image
import math
import glob
from pathlib import Path


SUB_DIR = 'toei-5300'


color_palette = [(0,0,0),(255,0,0),(0,255,0),(255,127,0)]   # black, red, green, orange

def get_approximate_color(c):
    min_distance = 99999
    index = 0
    color_index = 0
    for cp in color_palette:
        distance = math.sqrt( (cp[0]-c[0])*(cp[0]-c[0])+(cp[1]-c[1])*(cp[1]-c[1])+(cp[2]-c[2])*(cp[2]-c[2])) 
        if distance < min_distance:
            min_distance = distance
            color_index = index
        index += 1
    return color_palette[color_index]


def convert_approximate_color(file_name):
    im = Image.open(file_name)  # 画像を開く
    im = im.convert('RGB')

    start_x = 2
    start_y = 2
    step_pix = 3

    pic_width = int(math.floor((im.width - start_x ) / step_pix) + 1)
    pic_height = int(math.floor((im.height - start_y) / step_pix) + 1)

    pic = Image.new('RGB', (pic_width, pic_height) )

    print(pic_width)
    print(pic_height)

    for x in range(pic_width):
        for y in range(pic_height):
            pix_color = im.getpixel((start_x + x*step_pix, start_y + y*step_pix))
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
