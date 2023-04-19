from PIL import Image
from urllib.request import urlopen
import os
from pathlib import Path

while True: #asks if it will decode or encode
    print("decode(d) or encode(e)?")
    choice = input()
    if choice == 'e' or choice == 'd':
        break

if choice == 'e': #encoding a secret in an image
    while True:  # asks if it will decode or encode
        print("what data type are you trying to hide? image(i) or text(t)")
        choice = input()
        if choice == 'i' or choice == 't':
            break
    if choice == 'i':
        while True:  # asks if the image will come from a url or if it is already downloaded
            print("are you using a url link(u) or a downloaded image with a path on your computer(d) for the image you are trying to hide?")
            choice = input()
            if choice == 'u' or choice == 'd':
                break

        if choice == 'u':  # obtains image from url link
            print('what is your url?')
            path = input()
            secrimg = Image.open(urlopen(path))
        else:  # obtains image from computer
            print("what is the image path?")
            path = Path(input().strip().replace("\"", ""))
            secrimg = Image.open(path)


        while True:  # asks if the image will come from a url or if it is already downloaded
            print("are you using a url link(u) or a downloaded image with a path on your computer(d) for the image that will hide the other image?")
            choice = input()
            if choice == 'u' or choice == 'd':
                break
        if choice == 'u':  # obtains image from url link
            print('what is your url?')
            path = input()
            img = Image.open(urlopen(path))
        else:  # obtains image from computer
            print("what is the image path?")
            path = Path(input().strip().replace("\"", ""))
            img = Image.open(path)
        if (secrimg.height * secrimg.width+ 2*len("00000000000001") + len('{0:08b}'.format(secrimg.width)) + len('{0:08b}'.format(secrimg.height))) >= (img.height * img.width)//4 :
            secrimg = secrimg.resize((img.size[0]//3, img.size[1]//3))

        #converts all of the RGB(A) into binary
        secrdata = list(secrimg.getdata())
        secr = "1"
        if secrimg.mode == "RGBA":
            secr += '1'
        else:
            secr += '0'
        secr += '{0:08b}'.format(secrimg.width)
        secr += "00000000000001"
        secr += '{0:08b}'.format(secrimg.height)
        secr += '00000000000001'
        for x in secrdata:
            for a in x:
                secr += '{0:08b}'.format(a)
        print(secrimg.width)
        print(secrimg.height)
    if choice == 't':
        print("what info are you trying to hide?:")
        secret = input()
        secr = "00"
        for i in secret: #turns secret into binary
            secr += '{0:08b}'.format(ord(i))

        secr += "00000000000001"
        while True: #asks if the image will come from a url or if it is already downloaded
            print("are you using a url link(u) or a downloaded image with a path on your computer(d)?")
            choice = input()
            if choice == 'u' or choice == 'd':
                break

        if choice == 'u': #obtains image from url link
            print('what is your url?')
            path = input()
            img = Image.open(urlopen(path))
        else: #obtains image from computer
            print("what is the image path?")
            path = Path(input().strip().replace("\"", ""))
            img = Image.open(path)

    siz = img.size #gets image dimensions
    mod = img.mode == "RGBA" #get image type (ex. RGB, RGBA)
    data = list(img.getdata()) #gets all of the RGB(A) values and puts it in a list
    print(data)
    #algo is really simple, you take the least significant bit of each RGB value and make it match a bit of the secret
    #ex. if the RGB is (22, 34, 44) or (00010110, 00100010, 00101100) and the secret is 101
    #we change the RGB to (00010111, 00100010, 00101101) or (23,33,45) which looks the same to the original in our eyes but is different
    li = list(data[0])
    for x in range(len(secr)//2): #iterate through the secret
        if x % 3 == 0:
            li = list(data[x // 3])
        li[x % 3] = format(li[x % 3], "08b")[0:6] + (secr[x*2:x*2+2])
        if x % 3 == 2:
            nli = [int(li[i], 2) for i in range(3)]
            if mod :
                nli.append(li[3])
            data[x // 3] = tuple(nli) #turn the edited rgb list into a tuple and put back in data list
    if (len(secr)//2)%3 != 2:
        for x in range(3):
            if isinstance(li[x], int):
                li[x] = '{0:08b}'.format(li[x])
        nli = [int(li[i], 2) for i in range(3)]
        if mod:
            nli.append(li[3])
        data[((len(secr)//2)+2)//3] = tuple(nli)  # turn the edited rgb list into a tuple and put back in data list
    le = len(secr)

    #create the new image
    newimg = Image.new(img.mode, siz)
    newimg.putdata(data)
    newimg.show()
    zdat = list(img.getdata())
    ndat = list(newimg.getdata())
    while True:  #asks if image will be saved
        print("Would you like this image saved? (y or n)")
        choice = input()
        if choice == 'y' or choice == 'n':
            break

    if choice == 'y': #image will be saved
        while True:  # asks where it will be saved?
            print("Would you like it saved towards a specific path (p) or just downloaded with a specific name (n)?")
            choice = input()
            if choice == 'p' or choice == 'n':
                break

        if choice == 'p': #gets path and saves image there
            print("what is your path")
            path = Path(input().strip().replace("\"", ""))
            newimg.save(path)

        elif choice == 'n': #gets filename and saves image with it
            print('what is the filename (include .png/jpg)')
            name = input().strip().replace("\"", "")
            if os.name == "nt":
                downloadfolder = f"{os.getenv('USERPROFILE')}\\Downloads"
            else:  # PORT: For *Nix systems
                downloadfolder = f"{os.getenv('HOME')}/Downloads"
            print(downloadfolder + "\\" + name)
            newimg.save(downloadfolder + "\\" + name)
    #newimg.save("C:\\Users\\aksha\Downloads\\newimg.png")



if choice == 'd':
    while True: #loops until a valid option has been chosen
        print("are you using a url link(u) or a downloaded image with a path on your computer(d)?")
        choice = input()
        if choice == 'u' or choice == 'd':
            break

    if choice == 'u': #obtains image from url link
        print('what is your url?')
        path = input()
        img = Image.open(urlopen(path))
    else: #obtains image from computer
        print("what is the image path?")
        path = Path(input().strip().replace("\"" , "" ))
        img = Image.open(path)

    siz = img.size  # gets image dimensions
    mod = img.mode  # get image type (ex. RGB, RGBA)
    data = list(img.getdata())  # gets all of the RGB(A) values and puts it in a list
    secr = '{0:02b}'.format(data[0][0] % 4)
    check = secr[0] == "0"
    print(secr)
    if check:
        secr = ''
        condition = 0
        for x in range(1, len(data)*3): #gets the last 2 bits of data from each RGB value
            secr += '{0:02b}'.format(data[x // 3][x % 3] % 4)

            if data[x // 3][x % 3] % 4 == 0: #checks for the condition that ends transmission (0000000000001)
                condition += 1
            else:
                if condition >= 6:
                    break
                else:
                    condition = 0
    else:
        rgb = secr[1] == 0
        if(rgb):
            alpha = 3
        else:
            alpha = 4
        width = ""
        height = ""
        counter = 1
        condition = 0
        for x in range(1, len(data)*3, 1): #gets the last bit of data from each RGB value
            counter+=1
            width += '{0:02b}'.format(data[x // 3][x % 3] % 4)
            if data[x // 3][x % 3] % 4 == 0: #checks for the condition that ends transmission (0000000000001)
                condition += 1
            else:
                if condition >= 6:
                    break
                else:
                    condition = 0
        condition = 0
        for x in range(counter, len(data)*3, 1): #gets the last bit of data from each RGB value
            counter+=1
            height += '{0:02b}'.format(data[x // 3][x % 3] % 4)
            if data[x // 3][x % 3] % 4 == 0: #checks for the condition that ends transmission (0000000000001)
                condition += 1
            else:
                if condition >= 6:
                    break
                else:
                    condition = 0
        width = int(width[0:len(width)-14], 2)
        height = int(height[0:len(height) - 14], 2)
        secr = ''
        for x in range(counter, counter + (width*height*alpha*8)//2):  # gets the last 2 bits of data from each RGB value
            secr += '{0:02b}'.format(data[x // 3][x % 3] % 4)

        print(width)
        print(height)
        print(len(secr))
        print(width*height*8*alpha)
    if check:
        secr = secr[0:len(secr)-14] #removes unnecessary bits from the condition
        sec = ""
        for x in range(len(secr)//8): #turns binary into ascii/readable text
            sec += chr(int(secr[x*8:x*8+8], 2))
        print(sec)
        print(width*height)
    else:
        mode = ""
            # create the new image
        if rgb:
            mode = "RGB"
            dat = []
            for x in range(0, len(secr) // 24):
                dat.append(tuple([int(secr[x * 24:x * 24 + 8], 2), int(secr[x * 24 + 8:x * 24 + 16], 2),
                                  int(secr[x * 24 + 16:x * 24 + 24], 2)]))

        else:
            mode = "RGBA"
            dat = []
            for x in range(0, len(secr) // 32):
                dat.append(tuple([int(secr[x * 32:x * 32 + 8], 2), int(secr[x * 32 + 8:x * 32 + 16], 2),
                                  int(secr[x * 32 + 16:x * 32 + 24], 2), int(secr[x * 32 + 24:x * 32 + 32], 2)]))
        newimg = Image.new(mode, tuple([width, height]))
        newimg.putdata(dat)
        newimg.show()
        zdat = list(img.getdata())
        ndat = list(newimg.getdata())
        print(newimg.width)
        print(newimg.height)
        print(newimg.width * newimg.height)
        while True:  # asks if image will be saved
            print("Would you like this image saved? (y or n)")
            choice = input()
            if choice == 'y' or choice == 'n':
                break

        if choice == 'y':  # image will be saved
            while True:  # asks where it will be saved?
                print("Would you like it saved towards a specific path (p) or just downloaded with a specific name (n)?")
                choice = input()
                if choice == 'p' or choice == 'n':
                    break

            if choice == 'p':  # gets path and saves image there
                print("what is your path")
                path = Path(input().strip().replace("\"", ""))
                newimg.save(path)

            elif choice == 'n':  # gets filename and saves image with it
                print('what is the filename (include .png/jpg)')
                name = input().strip().replace("\"", "")
                if os.name == "nt":
                    downloadfolder = f"{os.getenv('USERPROFILE')}\\Downloads"
                else:  # PORT: For *Nix systems
                    downloadfolder = f"{os.getenv('HOME')}/Downloads"
                print(downloadfolder + "\\" + name)
                newimg.save(downloadfolder + "\\" + name)
        # newimg.save("C:\\Users\\aksha\Downloads\\newimg.png")
