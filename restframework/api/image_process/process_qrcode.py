import os
import qrcode
import cv2
import numpy as np
import imutils
from pyzbar.pyzbar import decode, ZBarSymbol

def create_qrcode(dst, data):
    qrcode_img = qrcode.make(data, border=1)
    qrcode_img.save(dst+"qrcode.jpg")
    # qrcode_img = cv2.imread(dst+"qrcode.jpg")
    # qrcode_img = cv2.resize(qrcode_img, (187, 187))
    # cv2.rectangle(qrcode_img, (0, 0), (qrcode_img.shape[1]-1, qrcode_img.shape[0]-1), (0, 0, 0), 5)
    # cv2.imwrite(dst+"qrcode.jpg", qrcode_img)
    return dst+"qrcode.jpg"

def read_qrcode(src, src_=None):
    img = cv2.imread(src)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width, channels = img.shape

    img_list = [img_gray,
                img_gray[height-85:height, width-85:width]]
    
    decoded = decode(img, symbols=[ZBarSymbol.QRCODE])
    img_succ = img
    num = 0
    if len(decoded) == 0:
        for i in img_list:
            num += 1
            for scalar in [1]:
                scaled_image = cv2.resize(i, None, fx=scalar, fy=scalar)
                for contrast in [0]:
                    alpha_c = 131 * (contrast + 127) / (127 * (131 - contrast))
                    gamma_c = 127 * (1 - alpha_c)
                    image_scaled = cv2.addWeighted(scaled_image, alpha_c, scaled_image, 0, gamma_c)
                    decoded = decode(image_scaled, symbols=[ZBarSymbol.QRCODE])
                    img_succ = image_scaled
                    cv2.imwrite('qr/__img/'+str(num)+'_'+str(scalar)+'_'+str(contrast)+'.jpg', image_scaled)
                    if decoded:
                        break
                if decoded:
                    break
            if decoded:
                break
            
    if src_ != None:
        for i in range(8, 12):
            cv2.imwrite(src_+"img_"+str(i)+".jpg", img_list[i])
        src_pass = src_+"pass/"
        if os.path.exists(src_pass) == False:
            os.makedirs(src_pass)
        src_fail = src_+"fail/"
        if os.path.exists(src_fail) == False:
            os.makedirs(src_fail)
        for d in decoded:
            cv2.rectangle(img_succ, (d.rect.left, d.rect.top), (d.rect.left+d.rect.width, d.rect.top+d.rect.height), (0, 0, 255), 2)
        if len(decoded) != 0:
            cv2.imwrite(src_pass+src.split("/")[-1], img_succ)
        else :
            cv2.imwrite(src_fail+src.split("/")[-1], img)

    if len(decoded) == 0:
        return False
    else:
        return decoded[0].data.decode('utf-8')

# if __name__ == '__main__':
#     create_qrcode("", "CE KMITL-1")