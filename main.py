import cv2 as cv
import numpy as np
import qrcode 

import pyzbar.pyzba


def generate_secret_key(num_pixels):

    return np.random.randint(0, 3, num_pixels)

def is_even(num):
    return num % 2 == 0

def flip(qr_rgb_value, img_rgb_value):
    # If RGB value of QR code is 0, then the image RGB value must be odd
    if qr_rgb_value == 0:
        if is_even(img_rgb_value):
            return img_rgb_value + 1
        else:
            return img_rgb_value
    # If RGB value of QR code is 255, then the image RGB value must be even
    elif qr_rgb_value == 255:
        if is_even(img_rgb_value):
            return img_rgb_value
        else:
            return img_rgb_value + 1
        

def encode_secret(img, secret, yield_secret_key=True):
    
    qr = qrcode.QRCode(border=0)
  
    qr.add_data(secret)
    qr.make()
    qr.make_image(fill_color="black", back_color="white").save("./images/qr.png")

    qr_img = cv.cvtColor(cv.imread("./images/qr.png"), cv.COLOR_BGR2RGB)

    qr_height, qr_width = qr_img.shape[:2]


    secret_key = generate_secret_key(qr_height * qr_width)

    print(len(secret_key))

    current = 0

    for i in range(0, qr_height - 1):
        for j in range(0, qr_width - 1):
            current += 1

       
            change = secret_key[current]

            img[i, j][change] = flip(qr_img[i, j][change], img[i, j][change])

    if yield_secret_key:
         return img, secret_key, qr_height, qr_width
    else:
        return img, qr_height, qr_width



def read_secret(img, secret_key, qr_height, qr_width):

    qr = np.zeros((qr_height, qr_width, 3), dtype=np.uint8)

    reader = QReader()

    current = 0
    for i in range(qr_height):
        for j in range(qr_width):

            current += 1

            change = secret_key[current]

            if is_even(img[i, j][change]):
                qr[i, j] = [255, 255, 255]
            else: 
                qr[i, j] = [0, 0, 0]

    
    return 


def main():

    base_img = cv.cvtColor(cv.imread("./images/profilepic.jpg"), cv.COLOR_BGR2RGB)

    modified_img, secret_key, qr_h, qr_w = encode_secret(base_img, "Hello Outernet!")

    cv.imwrite("./images/modified.png", modified_img)

    # Refactor read_secret to accept path to image

    secret = read_secret(modified_img, secret_key, qr_h, qr_w)

    print(secret)

if __name__ == "__main__":
    main()
