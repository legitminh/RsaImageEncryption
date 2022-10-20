from PIL import Image
import numpy as np
import rsa


# getting the image data
im = Image.open('Image/Input.png', 'r')
pix_val = np.asarray(im)
pix_val = np.array(pix_val)

# encoding the mesage
message = "Who are y0u so the w!@#$%欢迎广陵来到我国"
def EncodeStr(m):
    with open("Keys/Keys.txt") as f:
        data = f.readline()
        public_key = eval(f'rsa.{data}')
    return str(rsa.encrypt(m.encode('utf-8'), public_key))

message = EncodeStr(message)

def StrtoBin(m):# transformting encoded message into bits
    a = ''
    for i in m:
        a += '{:08b}'.format(ord(i))
    return a

message = StrtoBin(message)

# adding the data into the image
pos = 0
# for pos, bit in enumerate(message):#even number position, 2bit in a channel, 8bit in a pixel. Position / 8 is equal to x slot position absolute
#     pixelP = pos // 8
#     y = pixelP // im.size[0] #pixels // width
#     x = pixelP % im.size[0] #pixels remaider width
#     channel = pos % 8
#     pix_val[y, x, channel] >>= 2
#     pix_val[y, x, channel] <<= 2
#     pix_val[y, x, channel] |= int(message[pos:pos+2], 2)
#     pos += 1
for y in range(len(pix_val)):
    for x in range(len(pix_val[y])):
        for channel in range(len(pix_val[y, x])):
            pix_val[y, x, channel] >>= 2
            pix_val[y, x, channel] <<= 2
            pix_val[y, x, channel] |= int(message[pos:pos+2], 2)
            if pos < len(message) - 2:
                pos += 2
            else:
                break
if pos < len(message) - 2: # in message still not exhausted
    raise ValueError("Too large to encode in the image")

# storing image
new = Image.fromarray(pix_val, mode="RGBA")
pix_val = np.asarray(new)
pix_val = np.array(pix_val)
new.save("Image/Output.png")
