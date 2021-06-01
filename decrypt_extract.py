# Christopher Georgell
# Image Steganography Using Python
# CS 497 - Computing Capstone 
# City University of Seattle

import numpy as np
import cv2
import tkinter.scrolledtext as st
from tkinter import *
from PIL import Image, ImageTk
from cryptography.fernet import Fernet


#Open symmetric key from file to prepare for decryption
#################################################################

dkey = open("secret.key", "rb").read()
d = Fernet(dkey)


#Create function that previews the stego-image in the GUI
#Uses algorithm to extract embedded message from image,
#Decrypts the message, displays it on GUI, and saves it to file
#################################################################

final_image = 500, 350

def extract_decrypt():
    #opens the stego image for GUI use and declares the display size for the GUI
    file_load2 = Image.open("./crypt_stego.png")
    file_load2.thumbnail(final_image, Image.ANTIALIAS)

    #loads image into GUI and declares the preview location within window
    load_image2 = np.asarray(file_load2)
    load_image2 = Image.fromarray(np.uint8(load_image2))
    preview2 = ImageTk.PhotoImage(load_image2)
    image2 = Label(gui, image = preview2)
    image2.image = preview2
    image2.place(x=50, y=50)

    #opens the image for message extraction and decryption
    image = cv2.imread("./crypt_stego.png")
    
    #extract the LSB from every pixel value
    #If EOF bit is present, stop
    bits = []
    stop = False
    for index_y, y in enumerate(image):
        y.tolist()
        #print(x)
        for index_z, z in enumerate(y):
            if((index_z) % 3 == 2):
                bits.append(bin(z[0])[-1])

                bits.append(bin(z[1])[-1])

                if(bin(z[2])[-1] == '1'):
                    stop = True 
                    break
            else:
                bits.append(bin(z[0])[-1])

                bits.append(bin(z[1])[-1])

                bits.append(bin(z[2])[-1])

        if(stop):
            break
        
    #print(bits)
    message2 = []
    for i in range(int((len(bits)+1)/8)):
        message2.append(bits[i*8:(i*8+8)])
    #print(message)
    #convert message from binary 
    message2 = [chr(int(''.join(i), 2)) for i in message2]
    #print("Extracted  Message: ", message)
    message2 = ''.join(message2)
    print("Extracted Encrypted Message: ", message2)

    #decrypt the secret message using the symmetric encryption key 
    decrypt = d.decrypt(message2.encode())
    print("Decrypted Message: ", decrypt)
   
    #save the message to a file 
    secret_message = open("MySecret.txt", "w")
    secret_message.write(decrypt.decode())

    #display the message within the GUI
    print_message = st.ScrolledText(gui, width = 48, height = 8, font = ("Times New Roman", 15))

    print_message.grid(column = 0, pady = 10, padx = 10)

    print_message.insert(END, decrypt)

    print_message.configure(state = 'disabled')
    print_message.place(x = 50, y = 375)


#Create GUI for extraction and decryption use
#################################################################

#declare GUI size, color, and title
gui = Tk()
gui.configure(background= "dark slate gray") 
gui.title("Extract and Decrypt Message")
gui.geometry('600x600')

#create button that calls extract_decrypt function 
ext_dec = Button(gui, text = "Start Extraction and Decryption", bg = "black", fg = "white", command = extract_decrypt)
ext_dec.place(x = 225, y = 10)
gui.mainloop()