import qrcode
import cv2
from pyzbar.pyzbar import decode

def create_qrcode(dst, data):
    qrcode_img = qrcode.make(data, border=1)
    qrcode_img.save(dst+"qrcode.jpg")
    qrcode_img = cv2.imread(dst+"qrcode.jpg")
    qrcode_img = cv2.resize(qrcode_img, (187, 187))
    cv2.rectangle(qrcode_img, (0, 0), (qrcode_img.shape[1]-1, qrcode_img.shape[0]-1), (0, 0, 0), 5)
    cv2.imwrite(dst+"qrcode.jpg", qrcode_img)
    return dst+"qrcode.jpg"

def read_qrcode(src):
    img = cv2.imread(src)
    decoded = decode(img)
    return decoded[0].data.decode("utf-8")

# if __name__ == '__main__':
#     create_qrcode("", "CE KMITL-1")