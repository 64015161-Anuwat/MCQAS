# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import sys

def get_sorted_box(cont):
    rect = cv2.minAreaRect(cont)
    box = cv2.boxPoints(rect)
    if box.shape[0] < 4:
        return (None, None)
    
    a = np.array([(box[0][0], box[0][1]), 
                  (box[1][0], box[1][1]), 
                  (box[2][0], box[2][1]), 
                  (box[3][0], box[3][1])])
    ind = a[a[:,0].argsort()]
    ind1, ind2 = np.split(ind, 2)
    ind1 = ind1[ind1[:,1].argsort()]
    ind2 = ind2[ind2[:,1].argsort()]
    a_sorted = np.concatenate((ind1, ind2)).astype(int)
    a_sorted = a_sorted.astype(int) # Convert MatLike object to integer value

    return (a_sorted, box)

def process_qtn(srcpath, dstpathp1, dstpathp3, file, p1, indpart1, indpart2):
    try:
        part1 = None
        part2 = None
        other_list = []
        part3 = None
        img = cv2.imread(srcpath+file)
        height, width, channels = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        kernel = np.ones((7,7),np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        cv2.imwrite("1.jpg", thresh)
        
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
        for cont in contours:
            area = cv2.contourArea(contours[c])
            if area > 175000 and area < 200000:
                a_sorted, box = get_sorted_box(cont)
                if area < b and a_sorted is not None:
                    cropimg1 = img[a_sorted[0][1] :a_sorted[1][1] , a_sorted[0][0] :a_sorted[2][0] ]
                    d1+=1
                b = area
            c=c+1

        err1=0
        if d1==0:
            err1+=1

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
                err1="ไม่พบส่วนที่ 1 ของแบบสอบถามที่ไฟล์: "+file+" หรือ รูปภาพไม่ถูกต้อง"
            else:
                l = int(round(height1/5.0))
                s = int(round(26/100.0 * width1))
                b= int(round(41/100.0 * 400.0))
                x=30
                count = 0
                part1 = []
                n=0

                other_chk = False
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
                            if str("p1"+str(r+1)+str(q+1)) in p1:
                                other_chk = True
                                other = cropimg1[0+(l*r):l+(l*r), s+(b*q):s+(b*q)+b+20]
                                path = dstpathp1+'หัวข้อที่ '+str(r+1)+"/"+'ตัวเลือกที่ '+str(q+1)+"/"
                                other_list.append('หัวข้อที่ '+str(r+1)+"/"+'ตัวเลือกที่ '+str(q+1)+"/"+"p1"+str(r+1)+str(q+1)+"_"+file)
                                os.makedirs(path, exist_ok=True)
                                cv2.imwrite(path+"p1"+str(r+1)+str(q+1)+"_"+file, other)
                    if other_chk:
                        other_chk = False
                    else:
                        other_list.append("")

                    if count == 0 :
                        part1.append([])
                        part1[r].append(r+1)
                        part1[r].append("n")
                    count = 0
                    n=0
        else:
            err1="ไม่พบส่วนที่ 1 ของแบบสอบถามที่ไฟล์: "+file+" หรือ รูปภาพไม่ถูกต้อง"

        err2=0
        cropimg2 = img[540:1259,704:950]
        height2, width2, channels = cropimg2.shape
        gray = cv2.cvtColor(cropimg2, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
        linek = np.ones((5,5),np.uint8)
        thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, linek ,iterations=1)
        cv2.rectangle(thresh,(2,2),(width2-3,height2-3),(255,255,255),5)
        # cv2.imwrite("1.jpg",thresh)

        if width2 > 255 or  width2 < 235:
            err2+=1
        if height2 > 730 or height2 < 710:
            err2+=1

        if err2!=0:
            err2="ไม่พบส่วนที่ 2 ของแบบสอบถามที่ไฟล์: "+file+" หรือ รูปภาพไม่ถูกต้อง"
        else:
            col = int(round(width2/6.0))
            row = int(round(height2/18.0))
            count = 0
            part2 = []
            n=0

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

        a_sorted3 = [[704,540],[ 703,1259],[950,541],[948,1260]]
        mask = np.zeros(img.shape[:2], np.uint8)
        mask[a_sorted3[1][1]+45:height-15, 15:width-100] = 255
        masked_img3 = cv2.bitwise_and(img,img,mask = mask)
        gray = cv2.cvtColor(masked_img3, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        hist_mask = cv2.calcHist([thresh],[0],mask,[2],[0,256])
        if hist_mask[0] > 4500:
            cropimg3=img[a_sorted3[1][1]+10 :height-15 , 15 :width-100]
            part3 = "p3_"+file
            cv2.imwrite(dstpathp3+"p3_"+file,cropimg3)

        chk_err = True
        if err1 != 0 or err2 != 0:
            chk_err = False
        if err1 == 0: err1 = None
        if err2 == 0: err2 = None
        err=[chk_err, err1, err2]

        return (err,part1,part2,other_list,part3)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        return "Error Line "+str(exc_tb.tb_lineno if exc_tb else None)+" : "+str(e)+" at file: "+file
    
# if __name__ == '__main__':
#     indpart2 = [[], [], [], [], [], [], [], [], [], [], []]
#     print(processinf("","","","pre_infsheet.jpg",["p124", "p133", "143", "p153"],[[1, 2], [1, 2, 3, 4], [1, 2, 3], [1, 2, 3], [1, 2, 3]],[[], [], [], [], [], [], [], [], [], [], []]))
