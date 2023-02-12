from PIL import Image
import math

file_name = './1.gif'
im = Image.open(file_name)  # 画像を開く
im = im.convert('RGB')

start_x = 2
start_y = 2
step_pix = 3
background_color = (51,51,51)

pic_width = int(math.floor((im.width - start_x ) / step_pix) + 1)
pic_height = int(math.floor((im.height - start_y) / step_pix) + 1)

pic = Image.new('RGB', (pic_width, pic_height) )

print(pic_width)
print(pic_height)

for x in range(pic_width):
    for y in range(pic_height):
        pix_color = im.getpixel((start_x + x*step_pix, start_y + y*step_pix))
        if  pix_color == background_color:
            pic.putpixel((x,y), (0,0,0))
        else:
            pic.putpixel((x,y), pix_color)

#pic.show()
pic.save( file_name + '_.bmp', 'bmp')