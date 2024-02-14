# -*- coding: utf-8 -*-
import cv2
import numpy as np
import math
import os
import sys

def process_qtn(srcpath, dstpathp1, dstpathp3, file, p1, indpart1, indpart2):
    try:
        img = cv2.imread(srcpath+file)
        height, width, channels = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        kernel = np.ones((7,7),np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        mask = np.zeros(thresh.shape[:2], np.uint8)
        mask[200:450, 0:width] = 255
        masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)

        mask = np.zeros(thresh.shape[:2], np.uint8)
        mask[500:height-100, 600:width] = 255
        masked_img2 = cv2.bitwise_and(thresh,thresh,mask = mask)

        contours, hierarchy = cv2.findContours(masked_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        b=1000000
        c=0
        d1=0

        cropimg1 = None
        for a in contours:
            area = cv2.contourArea(contours[c])
            if area < 200000 and area > 175000:
                rect = cv2.minAreaRect(contours[c])
                boxc = cv2.boxPoints(rect)
                boxc = boxc.astype(int)

                a = np.array([(boxc[0][0], boxc[0][1]), (boxc[1][0], boxc[1][1]), (boxc[2][0], boxc[2][1]), (boxc[3][0], boxc[3][1])])
                ind = a[a[:,0].argsort()]
                ind1, ind2 = np.split(ind, 2)
                ind1 = ind1[ind1[:,1].argsort()]
                ind2 = ind2[ind2[:,1].argsort()]
                a_sorted = np.concatenate((ind1, ind2))

                if area < b:
                    cropimg1 = img[a_sorted[0][1] :a_sorted[1][1] , a_sorted[0][0] :a_sorted[2][0] ]
                    d1+=1
                b = area
            c=c+1

        err1=0
        if d1==0:
            err1+=1

        linek = np.ones((3,3),np.uint8)
        thresh=cv2.morphologyEx(masked_img2, cv2.MORPH_CLOSE, linek ,iterations=1)

        cropimg2 = img[540:1259,704:950]
        a_sorted3 = [[704,540],[ 703,1259],[950,541],[948,1260]]
        c=1
        d2=1
        err2=0
        if d2==0:
            err2+=1

        mask = np.zeros(img.shape[:2], np.uint8)
        mask[a_sorted3[1][1]+50:height-15, 15:width-15] = 255
        masked_img3 = cv2.bitwise_and(img,img,mask = mask)
        gray = cv2.cvtColor(masked_img3, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        ke = np.ones((4,1),np.uint8)
        cv2.imwrite(srcpath+"path3.1"+file,thresh)
        thresh=cv2.morphologyEx(masked_img3, cv2.MORPH_CLOSE, ke ,iterations=1)
        cv2.imwrite(srcpath+"path3.2"+file,thresh)
        hist_mask = cv2.calcHist([thresh],[0],mask,[2],[0,256])
        if hist_mask[0] > 3000:
            cropimg3=img[a_sorted3[1][1]+10 :height-15 , 15 :width-100 ]
            cv2.imwrite(dstpathp3+"p3_"+file,cropimg3)

        if cropimg1 is not None:
            height1, width1, channels = cropimg1.shape
            gray = cv2.cvtColor(cropimg1, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
            linek = np.ones((5,5),np.uint8)
            thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, linek ,iterations=1)
            cv2.rectangle(thresh,(2,2),(width1-3,height1-3),(255,255,255),5)

            if width1 > 910 or  width1 < 890:
                err1+=1
            if height1 > 210 or height1 < 190:
                err1+=1

            if err1!=0:
                err1="Image File : "+file+" has something error in part1 ."
        else:
            err1="ไม่พบส่วนที่ ๅ ของแบบสอบถามที่ไฟล์: "+file+" หรือ รูปภาพไม่ถูกต้อง"

        l = int(round(height1/5.0))
        s = int(round(26/100.0 * width1))
        b= int(round(41/100.0 * 400.0))
        x=30
        count = 0
        part1 = []
        n=0

        if err1 == 0 and cropimg1 is not None:
            for r in range(len(indpart1)):
                for q in range(len(indpart1[r])):
                    mask = np.zeros(thresh.shape[:2], np.uint8)
                    mask[0+(l*r):l+(l*r), s+(b*q):s+(b*q)+x] = 255
                    masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)
                    hist_mask = cv2.calcHist([thresh],[0],mask,[2],[0,256])
                    if hist_mask[0] > 40 :
                        if n == 0 :
                            part1.append([])
                            part1[r].append(r+1)
                            n+=1
                        part1[r].append(q+1)
                        count = count +1
                        if any("p1"+str(r+1)+str(q+1) in s for s in p1):
                            other = cropimg1[0+(l*r)-15 :l+(l*r) ,s+(b*q):s+(b*q)+b+20 ]
                            path = dstpathp1+'หัวข้อที่ '+str(r+1)+"/"+'ตัวเลือกที่ '+str(q+1)+"/"
                            os.makedirs(path, exist_ok=True)
                            cv2.imwrite(path+"p1"+str(r+1)+str(q+1)+"_"+file, other)

                if count == 0 :
                    part1.append([])
                    part1[r].append(r+1)
                    part1[r].append("n")
                count = 0
                n=0

        height2, width2, channels = cropimg2.shape
        gray = cv2.cvtColor(cropimg2, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
        linek = np.ones((5,5),np.uint8)
        thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, linek ,iterations=1)
        cv2.rectangle(thresh,(2,2),(width2-3,height2-3),(255,255,255),5)

        if width2 > 255 or  width2 < 235:
            err2+=1
        if height2 > 730 or height2 < 710:
            err2+=1

        if err2!=0:
            err2="Image File : "+file+" has something error in part2 ."

        col = int(round(width2/6.0))
        row = int(round(height2/18.0))
        count = 0
        part2 = []
        n=0

        if err2 == 0:
            for r in range(len(indpart2)):
                for q in range(6):
                    mask = np.zeros(thresh.shape[:2], np.uint8)
                    mask[0+(row*r):row+(row*r), 0+(col*q):col+(col*q)] = 255
                    masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)
                    hist_mask = cv2.calcHist([thresh],[0],mask,[2],[0,256])
                    if hist_mask[0] > 40 :
                        if n == 0 :
                            part2.append([])
                            part2[r].append(r+1)
                            n+=1
                        part2[r].append(abs(q-5))
                        count = count +1

                if count == 0 :
                    part2.append([])
                    part2[r].append(r+1)
                    part2[r].append("n")
                count = 0
                n=0

        chk_err = True
        if err1 != 0 or err2 != 0:
            chk_err = False
        if err1 == 0: err1 = None
        if err2 == 0: err2 = None
        err=[chk_err, err1, err2]

        return (err,part1,part2)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        return "Error Line "+str(exc_tb.tb_lineno if exc_tb else None)+" : "+str(e)+" at file: "+file
    
# if __name__ == '__main__':
#     indpart2 = [[], [], [], [], [], [], [], [], [], [], []]
#     print(processinf("","","","pre_infsheet.jpg",["p124", "p133", "143", "p153"],[[1, 2], [1, 2, 3, 4], [1, 2, 3], [1, 2, 3], [1, 2, 3]],[[], [], [], [], [], [], [], [], [], [], []]))
