import rsa
with open("Keys/Keys.txt","w") as f:
    keys = rsa.newkeys(512)
    f.writelines(str(keys[0])+'\n')
    f.writelines(str(keys[1]))