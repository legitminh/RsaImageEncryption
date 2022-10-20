from PIL import Image
import numpy as np
import rsa


# getting the keys
with open("Keys/Keys.txt") as f:
    f.readline()
    data = f.readline()
    private_key = eval(f'rsa.{data}')

# getting data from the image
im = Image.open('Image/Output.png', 'r')
pix_val = np.asarray(im)
pix_val = np.array(pix_val)

# getting bits from the image & storing them as an int
bit_message: int = 0
for y in range(len(pix_val)):
    for x in range(len(pix_val[y])):
        for channel in range(len(pix_val[y, x])):
            # if pix_val[y, x, channel] % 2 == 0:
            #     bit_message <<= 1
            #     bit_message |= 0
            # else:
            #     bit_message <<= 1
            #     bit_message |= 1
            bit_message <<= 2
            bit_message |= int(bin(pix_val[y, x, channel] % 4),2)


# transforming bits into hex
message: str = str(bin(bit_message))[2:]
while len(message) % 8 != 0:
    message = '0' + message
text = ''
end = -1
count_of_quotes = 0
for character in range(len(message)):
    if character < end:
        continue
    end = character+8
    n = int(message[character:character + 8], 2)
    if chr(n) == "'" or chr(n) == '"':
        count_of_quotes += 1
    text += chr(n)
    if count_of_quotes == 2:
        break

# decoding that hex
decoded = eval(f'rsa.decrypt({text}, private_key)')
print(decoded)