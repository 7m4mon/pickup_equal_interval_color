
LEDギャラリー[https://w.atwiki.jp/led-gallery/]  
の画像を保存したフォルダに対して一括でサイズの縮小＆減色するプログラム。  
3 ピクセル毎にピックアップして、予め設定したパレットから近似色を選ぶ。  
減色方法はパレットからのピックアップか、計算が選べるようになっています。  
パレットは [led-gallery(R,G,B), led-matrix(R,G,B)]の順になっていて  
ピックアップした色を最も近い色[0]に対応する色[1]に置き換えます。  
計算する場合、1/4 scan (64ずつ) で切り捨てた値にします。  
実際に Pico LED Matrix で表示させるには JTrimによる後処理（256色化）が必要です。  

## 処理の流れ
1. led-galleryから画像をダウンロード
1. アニメーションGIFは split_gif.py でpngに分解
1. PNGを pickup_equal_interval_color.py でリサイズ＆減色したBMPにする
1. JTrim でフォルダ一括256色化する
1. Raspberry Pi Pico の /bmps/に転送
1. Pico LED Matrix で表示
