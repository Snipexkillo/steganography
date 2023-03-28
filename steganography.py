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

    print("what info are you trying to hide?:")
    secret = input()
    secr = ''
    for i in secret: #turns secret into binary
        secr += format(ord(i), "08b")
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
    mod = img.mode #get image type (ex. RGB, RGBA)
    data = list(img.getdata()) #gets all of the RGB(A) values and puts it in a list

    #algo is really simple, you take the least significant bit of each RGB value and make it match a bit of the secret
    #ex. if the RGB is (22, 34, 44) or (00010110, 00100010, 00101100) and the secret is 101
    #we change the RGB to (00010111, 00100010, 00101101) or (23,33,45) which looks the same to the original in our eyes but is different

    for x in range(len(secr)): #iterate through the secret

        if secr[x] == "0" and data[x // 3][x%3]%2==1: #LSB changes only if a change needs to be made
            li = list(data[x//3]) #get the rgb value as a list
            li[x%3] -= 1 #edit
            data[x//3] = tuple(li) #turn the edited rgb list into a tuple and put back in data list

        elif secr[x] == "1" and data[x // 3][x%3]%2==0: #LSB changes only if a change needs to be made
            li = list(data[x // 3]) #get the rgb value as a list
            li[x % 3] += 1 #edit
            data[x // 3] = tuple(li) #turn the edited rgb list into a tuple and put back in data list

    le = len(secr)
    # a simple way to end transmission, if you get 12 0's and a 1 then decoder knows transmission is over
    for x in range(12): #adds the 12 0's
        li = list(data[(le + x) // 3])
        if li[(le + x) %3] %2 == 1:
            li[(le + x) % 3] -= 1
            data[(le + x) // 3] = tuple(li)
    li = list(data[(le + 12) // 3]) #adds the one
    li[(le + 12) % 3] = 1
    data[(le + 12) // 3] = tuple(li)

    #create the new image
    newimg = Image.new(mod, siz)
    newimg.putdata(data)
    newimg.show()

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
            print(downloadfolder + name)
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


    secr = ""
    condition = 0
    for x in range(len(data)*3): #gets the last bit of data from each RGB value
        secr += str(data[x // 3][x % 3] % 2)
        if data[x // 3][x % 3] % 2 == 0: #checks for the condition that ends transmission (0000000000001)
            condition += 1
        else:
            if condition >= 12:
                break
            else:
                condition = 0

    secr = secr[0:len(secr)-13] #removes unnecessary bits from the condition
    sec = ""
    for x in range((len(secr)+7)//8): #turns binary into ascii/readable text
        sec += chr(int(secr[x*8:x*8+8], 2))
    print(sec) #prints decoded secret
