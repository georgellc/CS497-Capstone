# Christopher Georgell
# Image Steganography Using Python
# CS 497 - Computing Capstone 
# City University of Seattle

import math
import numpy as np
import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet

global file_path


#Encryption key generation
##################################################

#generate encryption key and save to file for decryption use
ekey = Fernet.generate_key()
e = Fernet(ekey)
with open("secret.key", "wb") as key_file:
    key_file.write(ekey)

#Message encryption and embedding into image
##################################################

def encrypt_embed():
    global file_path

    #Retrieve message from GUI text input
    secret = message.get(1.0, "end-1c")
    #print("Message Before Encryption: ",  secret)
    print("Length of Plain Text Message: ", len(secret))

    #Convert message into bytes and encrypt
    encrypt = e.encrypt(secret.encode())
    #print("Message After Encryption: ", encrypt)
    print("Length of Encrypted Message: ", len(encrypt))

    #Read image from chosen file path
    image = cv2.imread(file_path)
    #print(image[1:10])

    
    #Convert encryption into binary format
    encrypt = [format(i, '08b') for i in encrypt]
    #print("Encrypted Message Converted to Binary: ", encrypt)

    #Determine image rows, columns, and channels 
    _, width, _ = image.shape
    print("Image Dimensions: ", image.shape)
    print("width: ", width)
    #Determine pixels required for the encrypted message
    pixels = len(encrypt) * 3
    print("pixels: ", pixels)
    #Determine rows required for the encrypted message
    rows = pixels/width
    rows = math.ceil(rows)
    print("rows:", rows)
    

    count = 0
    charCount = 0
    #Algorithm to embed 1 byte within every 3 pixels
    #If pixel byte value is even and bit to be stored is 1, then subtract 1 
    #If pixel byte value is odd and bit to be stored is 0, then subtract 1
    #Maintain count of characters using count variable
    #If index number is 7, see if there is still characters to be stored
    #If no, mark the EOF as 1 and stop. If yes, mark EOF as 0 and continue
    for i in range(rows):
        while(count < width-1 and charCount < len(encrypt)):
            num_char = encrypt[charCount]
            charCount += 1
            for index_x, x in enumerate(num_char):
                if((x == '1' and image[i][count][index_x % 3] % 2 == 0) or (x == '0' and image[i][count][index_x % 3] % 2 == 1)):
                    image[i][count][index_x % 3] -= 1
                if(index_x % 3 == 2):
                    count += 1
                if(index_x == 7):
                    if(charCount*3 < pixels and image[i][count][2] % 2 == 1):
                        image[i][count][2] -= 1
                    if(charCount*3 >= pixels and image[i][count][2] % 2 == 0):
                        image[i][count][2] -= 1
                    count += 1
        count = 0
        
    #Save stegonagraphy image to a file and display success message on GUI
    cv2.imwrite("crypt_stego.png", image)
    completion = Label(gui, text="Message Encryption \nand Embedding Successful!",
                bg="dark slate gray", fg = "dark orange", font=("Times New Roman", 20, "bold"))
    completion.place(x=160, y=350)


#Image selection from GUI
##################################################

image_size = 300, 300

def get_image():
    global file_path
    #Use tkinter to define file path using a dialog allowing user to choose image
    file_path = filedialog.askopenfilename()
    #Set the image thumnail size
    file_load = Image.open(file_path)
    file_load.thumbnail(image_size, Image.ANTIALIAS)
    #Convert image to numpy to allow it to be used in the algorithm 
    load_image = np.asarray(file_load)
    load_image = Image.fromarray(np.uint8(load_image))
    #Preview the image on the GUI
    preview = ImageTk.PhotoImage(load_image)
    image = Label(gui, image = preview)
    image.image = preview
    image.place(x=20, y=80)


#GUI creation
##################################################

#Define size, color, and title of GUI window
gui = Tk()
gui.configure(bg = "dark slate gray")
gui.title("Image Steganography")
gui.geometry("600x500")

#create button to call get_image function allowing user to choose image
choose_image = Button(gui, text = "Choose Image to Embed", bg = "black", fg = "white", command = get_image)
choose_image.place(x=250, y=10)

#create text field with title to allow user to enter desired message
msgFrame = Frame(gui, borderwidth=1, relief = "sunken")
message = Text(msgFrame, wrap = WORD, height = 13, width = 30, borderwidth = 0)

scrollbar = Scrollbar(msgFrame, orient = "vertical", command = message.yview)
message['yscroll'] = scrollbar.set

scrollbar.pack(side="right", fill="y")
message.pack(side="left", fill="both", expand = True)

msgFrame.place(x = 340, y = 80)

txt_label = Label(gui, text = "Enter Message Below", bg = "dark slate gray", font = ("Times New Roman", 14, "bold"))
txt_label.place(x = 375, y = 50)

#create button to execute the algorithm and encrypt and embed the message within the image
embed_button = Button(gui, text = "Click to Embed Image", bg = "black", fg = "white", command = encrypt_embed)
embed_button.place(x = 400, y = 300)

gui.mainloop()