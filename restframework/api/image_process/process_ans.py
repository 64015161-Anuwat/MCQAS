import cv2
import numpy as np
import sys, os

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

def get_true_pix(thresh, mask):
    hist_mask = cv2.calcHist([thresh],[0],mask,[2],[0,256])
    true_pix = (hist_mask[0] / (hist_mask[0]+hist_mask[1])) * 100
    return (true_pix, hist_mask)


def process_ans(srcpath, filename, num_choice, debug=False):
    try:
        true_pix_check = 0.38*60
        threshold_ans = 190
        error_table_std = None
        error_table_sub = None
        error_table_ans = None

        img = cv2.imread(srcpath+filename)
        height, width, channels = img.shape

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # thresh = cv2.Canny(thresh, 0, 180)
        ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        # kernel = np.ones((5,5),np.uint8)
        # thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,kernel)
        # kernel1 = np.ones((2,2),np.uint8)
        # thresh = cv2.erode(thresh,kernel1,iterations = 1)

        mask = np.zeros(thresh.shape[:2], np.uint8)
        mask[290:height, 0:500] = 255
        masked_img1 = cv2.bitwise_and(thresh,thresh,mask = mask)
        # cv2.imshow("1", thresh)
        # cv2.waitKey(0)

        mask = np.zeros(thresh.shape[:2], np.uint8)
        mask[20:60, 480:530] = 255
        masked_img2 = cv2.bitwise_and(thresh,thresh,mask = mask)
        # cv2.imshow("2", masked_img2)
        # cv2.waitKey(0)

        contours, hierarchy = cv2.findContours(masked_img1, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        table_std = None
        table_sub = None
        for cont in contours:
            area = cv2.contourArea(cont)
            if area > 140000 and area < 160000:
                a_sorted, box = get_sorted_box(cont)
                if a_sorted is not None:
                    if a_sorted[0][1] < 400:
                        table_std = img[a_sorted[0][1]+3:a_sorted[1][1]-3, a_sorted[0][0]+2:a_sorted[2][0]-3]
                    elif a_sorted[0][1] > 400:
                        table_sub = img[a_sorted[0][1]+3:a_sorted[1][1]-3, a_sorted[0][0]+2:a_sorted[2][0]-3]
            elif area > 300000 and area < 340000 :
                a_sorted, box = get_sorted_box(cont)
                if a_sorted is not None:
                    temp = int(round(((a_sorted[1][1] - a_sorted[0][1]) / 2.0)))
                    temp = a_sorted[0][1] + temp
                    table_std = img[a_sorted[0][1] +2:temp -3, a_sorted[0][0] +2:a_sorted[2][0] -2]
                    table_sub = img[temp +3:a_sorted[1][1] -2, a_sorted[0][0] +2:a_sorted[2][0] -2]
                
        # if table_std is not None: cv2.imwrite("image/test/section_1/Section_1_"+filename.split(".")[0]+".jpg", table_std)
        # if table_sub is not None: cv2.imwrite("image/test/section_2/Section_2_"+filename.split(".")[0]+".jpg", table_sub)

        contours, hierarchy = cv2.findContours(masked_img2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        table_ans = None
        for cont in contours:
            area = cv2.contourArea(cont)
            if area > 100 and area < 300:
                a_sorted, box = get_sorted_box(cont)
                if a_sorted is not None:
                    table_ans = img[0:height, a_sorted[0][0]:width]

        # if table_ans is not None: cv2.imwrite("image/test/section_3/Section_3_"+filename.split(".")[0]+".jpg", table_ans)
        

        ##########################################################################

        std_id = []
        sec = []
        if table_std is not None:
            height1, width1, ch = table_std.shape
            gray = cv2.cvtColor(table_std, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, threshold_ans, 255, cv2.THRESH_BINARY)
            kernel = np.ones((5,5),np.uint8)
            thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel ,iterations=1)
            # cv2.imshow('BILL', thresh)
            # cv2.waitKey(0)

            x = int(round(width1/float(15)))
            y = 25
            
            # for col in range(15):
            #     for row in range(10):
            #         cv2.rectangle(thresh,(0+x*col,65+y*row),(x*col+x,90+y*row),(255,0,0),1)

            # cv2.imshow('BILL', thresh)
            # cv2.waitKey(0)

            count = 0
            for col in range(15):
                if col < 13 : std_id.append([])
                else : sec.append([])

                for row in range(10):
                    mask = np.zeros(thresh.shape[:2], np.uint8)

                    y_start = 65+y*row
                    y_end = 90+y*row-1

                    x_start = x*col+4
                    x_end = x*col+x

                    mask[y_start:y_end, x_start:x_end] = 255
                    # hist_mask = cv2.calcHist([thresh],[0],mask,[2],[0,256])
                    # print(hist_mask[0])
                    true_pix, hist_mask = get_true_pix(thresh, mask)
                    # masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)
                    # cv2.imshow('BILL', masked_img)
                    # cv2.waitKey(0)
                    if true_pix >= true_pix_check/2 :
                        count += 1
                        if col < 13 :
                            std_id[col].append(col+1)
                            std_id[col].append(row)
                        else :
                            sec[col%13].append((col%13)+1)
                            sec[col%13].append(row)
                        if debug == True:
                            cv2.putText(table_std, str(true_pix[0]), (x_start,y_start-3), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,0,255), 1)
                            cv2.rectangle(table_std,(x_start,y_start),(x_end,y_end),(0,0,255),1)
                    else : 
                        if debug == True:
                            cv2.putText(table_std, str(true_pix[0]), (x_start,y_start-3), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,255,0), 1)
                            cv2.rectangle(table_std,(x_start,y_start),(x_end,y_end),(0,255,0),1)

                if col < 13 :
                    if count == 0 :
                        std_id[col].append(col+1)
                        std_id[col].append("n")
                else :
                    if count == 0 :
                        sec[col%13].append((col%13)+1)
                        sec[col%13].append("n")
                count = 0
            
            if debug == True:
                isExist = os.path.exists(srcpath+"table_std_detect/")
                if isExist == False:
                    os.mkdir(srcpath+"table_std_detect/")
                cv2.imwrite(srcpath+"table_std_detect/table_std_"+filename, table_std)
            # print("student ID : "+str(std_id))
            # print("Section : "+str(sec))

        ##########################################################################

        seat_id = []
        sub_id = []
        ex_id = []
        if table_sub is not None:
            height2, width2, ch = table_sub.shape
            gray = cv2.cvtColor(table_sub, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, threshold_ans, 255, cv2.THRESH_BINARY)
            kernel = np.ones((5,5),np.uint8)
            thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel ,iterations=1)
            # cv2.rectangle(thresh,(3,3),(width2-3,height2-3),(255, 255, 255),5)
            # cv2.imshow('BILL', thresh)
            # cv2.waitKey(0)

            x= int(round(width2/float(15)))
            y = 25
            row_seat = ['A','B','C','D','E','F','G','H','I','J']

            # for r in range(15):
            #     for row in range(10):
            #         cv2.rectangle(thresh,(0+x*r,65+y*row),(x*r+x,90+y*row),(255,0,0),1)

            # cv2.imshow('BILL', thresh)
            # cv2.waitKey(0)

            count = 0
            for col in range(15):
                if col >= 0  and col < 5 : seat_id.append([])
                elif col > 4  and col < 13 : sub_id.append([])
                else : ex_id.append([])

                for row in range(10):
                    mask = np.zeros(thresh.shape[:2], np.uint8)

                    y_start = 65+y*row
                    y_end = 90+y*row-1

                    x_start = x*col+4
                    x_end = x*col+x-0
                    
                    mask[y_start:y_end, x_start:x_end] = 255
                    # masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)
                    # hist_mask = cv2.calcHist([thresh],[0],mask,[2],[0,256])
                    true_pix, hist_mask = get_true_pix(thresh, mask)
                    if true_pix >= true_pix_check/2 :
                        count += 1
                        if col == 0 :
                            seat_id[col].append(col+1)
                            seat_id[col].append(row_seat[row])
                        elif col > 0 and col < 5:
                            seat_id[col].append(col+1)
                            seat_id[col].append(row)
                        elif col > 4  and col < 13 :
                            sub_id[col%13 -5].append(((col%13)-5)+1)
                            sub_id[col%13 -5].append(row)
                        else :
                            ex_id[col%13].append((col%13)+1)
                            ex_id[col%13].append(row)
                        if debug == True:
                            cv2.putText(table_sub, str(true_pix[0]), (x_start,y_start-3), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,0,255), 1)
                            cv2.rectangle(table_sub,(x_start,y_start),(x_end,y_end),(0,0,255),1)
                    else : 
                        if debug == True:
                            cv2.putText(table_sub, str(true_pix[0]), (x_start,y_start-3), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,255,0), 1)
                            cv2.rectangle(table_sub,(x_start,y_start),(x_end,y_end),(0,255,0),1)

                if col >= 0 and col < 5 :
                    if count == 0 :
                        seat_id[col].append(col+1)
                        seat_id[col].append("n")
                elif col > 4  and col < 13 :
                    if count == 0 :
                        sub_id[col%13 -5].append(((col%13)-5)+1)
                        sub_id[col%13 -5].append("n")
                else :
                    if count == 0 :
                        ex_id[col%13].append((col%13)+1)
                        ex_id[col%13].append("n")
                count = 0

            if debug == True:
                isExist = os.path.exists(srcpath+"table_sub_detect/")
                if isExist == False:
                    os.mkdir(srcpath+"table_sub_detect/")
                cv2.imwrite(srcpath+"table_sub_detect/table_sub_"+filename, table_sub)
            # print("Seat ID : "+str(seat_id))
            # print("Subject ID : "+str(sub_id))
            # print("Exam ID : "+str(ex_id))

        ##########################################################################
        error_mkv = None
        error_mkvr = None
        error_mkh = None
        error_mkhb = None
        ans = []
        if table_ans is not None:
            height3, width3, channels = table_ans.shape
            gray = cv2.cvtColor(table_ans, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            mask = np.zeros(thresh.shape[:2], np.uint8)
            mask[10:height3-10, 0:25] = 255
            masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)
            kernel = np.ones((1,10),np.uint8)
            masked_img = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)
            contours, hierarchy = cv2.findContours(masked_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

            # print("mkv ==========================================")
            mkv1 = None
            mkv2 = None
            mkv3 = None
            mkv4 = None
            for cont in contours:
                area = cv2.contourArea(cont)
                epsilon = 0.01 * cv2.arcLength(cont, True)
                approx = cv2.approxPolyDP(cont, epsilon, True)
                if(area<200 and area>80 ):
                    a_sorted, box = get_sorted_box(approx)
                    if a_sorted is not None:
                    # print(a_sorted)
                        if  a_sorted[0][1] < 250 :
                            mkv1= (a_sorted[1][1] - a_sorted[0][1])/2.0
                            mkv1 = int(round(mkv1))
                            mkv1 = a_sorted[0][1] + mkv1
                            # print(mkv1)
                        elif a_sorted[0][1] > 250 and a_sorted[0][1] < 500 :
                            mkv2= (a_sorted[1][1] - a_sorted[0][1])/2.0
                            mkv2 = int(round(mkv2))
                            mkv2 = a_sorted[0][1] + mkv2
                            # print(mkv2)
                        elif a_sorted[0][1] >500 and a_sorted[0][1] <750 :
                            mkv3= (a_sorted[1][1] - a_sorted[0][1])/2.0
                            mkv3 = int(round(mkv3))
                            mkv3 = a_sorted[0][1] + mkv3
                            # print(mkv3)
                        elif a_sorted[0][1] >750 :
                            mkv4= (a_sorted[1][1] - a_sorted[0][1])/2.0
                            mkv4 = int(round(mkv4))
                            mkv4 = a_sorted[0][1] + mkv4
                            # print(mkv4)
            if mkv1 is None or mkv2 is None or mkv3 is None or mkv4 is None: error_mkv = "can't find mkv at "+filename

            mask = np.zeros(thresh.shape[:2], np.uint8)
            mask[10:height3-35, width3-25:width3] = 255
            masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)
            kernel = np.ones((1,10),np.uint8)
            thresh_morp = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)
            contours, hierarchy = cv2.findContours(thresh_morp, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

            # print("mkvr ==========================================")
            mkvr1 = None
            mkvr2 = None
            mkvr3 = None
            mkvr4 = None
            for cont in contours:
                area = cv2.contourArea(cont)
                epsilon = 0.01 * cv2.arcLength(cont, True)
                approx = cv2.approxPolyDP(cont, epsilon, True)
                if(area<200 and area>80 ):
                    a_sorted, box = get_sorted_box(approx)
                    if a_sorted is not None:
                        # print(a_sorted, area)
                        if  a_sorted[0][1] <250 :
                            mkvr1= (a_sorted[1][1] - a_sorted[0][1])/2.0
                            mkvr1 = int(round(mkvr1))
                            mkvr1 = a_sorted[0][1] + mkvr1
                            # print("mkvr1", mkvr1)
                        elif a_sorted[0][1] >250 and a_sorted[0][1] <500 :
                            mkvr2= (a_sorted[1][1] - a_sorted[0][1])/2.0
                            mkvr2 = int(round(mkvr2))
                            mkvr2 = a_sorted[0][1] + mkvr2
                            # print("mkvr2", mkvr2)
                        elif a_sorted[0][1] >500 and a_sorted[0][1] <750 :
                            mkvr3= (a_sorted[1][1] - a_sorted[0][1])/2.0
                            mkvr3 = int(round(mkvr3))
                            mkvr3 = a_sorted[0][1] + mkvr3
                            # print("mkvr3", mkvr3)
                        elif a_sorted[0][1] >750 :
                            mkvr4= (a_sorted[1][1] - a_sorted[0][1])/2.0
                            mkvr4 = int(round(mkvr4))
                            mkvr4 = a_sorted[0][1] + mkvr4
                            # print("mkvr4", mkvr4)
            if mkvr1 is None or mkvr2 is None or mkvr3 is None or mkvr4 is None: error_mkvr = "can't find mkvr at "+filename

            height3, width3, channels = table_ans.shape
            gray = cv2.cvtColor(table_ans, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            mask = np.zeros(thresh.shape[:2], np.uint8)
            mask[0:25, 10:width3-10] = 255
            masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)
            kernel = np.ones((10,1),np.uint8)
            thresh_morp = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)

            contours, hierarchy = cv2.findContours(thresh_morp, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            # print("mkh ==========================================")
            mkh1_2 = None
            mkh2_1 = None
            mkh2_2 = None
            mkh3_1 = None
            mkh3_2 = None
            mkh4_1 = None
            mkh4_2 = None
            for cont in contours:
                area = cv2.contourArea(cont)
                epsilon = 0.01 * cv2.arcLength(cont, True)
                approx = cv2.approxPolyDP(cont, epsilon, True)
                if(area<200 and area>80 ):
                    a_sorted, box = get_sorted_box(approx)
                    if a_sorted is not None:
                    # print(a_sorted)
                        if  a_sorted[0][0] <150 :
                            mkh1_2 = a_sorted[2][0]
                            # print(mkh1_2)
                        elif a_sorted[0][0] >150 and a_sorted[0][0] <375 :
                            mkh2_1 = a_sorted[0][0]
                            mkh2_2 = a_sorted[2][0]
                            # print(mkh2_1)
                            # print(mkh2_2)
                        elif a_sorted[0][0] >375 and a_sorted[0][0] <575 :
                            mkh3_1 = a_sorted[0][0]
                            mkh3_2 = a_sorted[2][0]
                            # print(mkh3_1)
                            # print(mkh3_2)
                        elif a_sorted[0][0] >575 :
                            mkh4_1 = a_sorted[0][0]
                            mkh4_2 = a_sorted[2][0]
                            # print(mkh4_1)
                            # print(mkh4_2)
            if mkh1_2 is None or mkh2_1 is None or mkh2_2 is None or mkh3_1 is None or mkh3_2 is None or mkh4_1 is None or mkh4_2 is None: error_mkh = "can't find mkh at "+filename

            mask = np.zeros(thresh.shape[:2], np.uint8)
            mask[0:50, 700:width3] = 255
            masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)
            kernel = np.ones((8,8),np.uint8)
            thresh_morp = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)

            contours, hierarchy = cv2.findContours(thresh_morp, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            # print("mkh5 ==========================================")
            mkh5_1 = None
            for cont in contours:
                area = cv2.contourArea(cont)
                epsilon = 0.01 * cv2.arcLength(cont, True)
                approx = cv2.approxPolyDP(cont, epsilon, True)
                if(area<200 and area>80 ):
                    a_sorted, box = get_sorted_box(approx)
                    if a_sorted is not None:
                        # print(a_sorted)
                        mkh5_1 = (a_sorted[2][0] - a_sorted[0][0]) / 4.0
                        mkh5_1 = int(round(mkh5_1))
                        mkh5_1 = a_sorted[0][0] + mkh5_1
                        # print(mkh5_1)

            mask = np.zeros(thresh.shape[:2], np.uint8)
            mask[height3-25:height3, 10:width3-33] = 255
            masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)
            kernel = np.ones((10,1),np.uint8)
            thresh_morp = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)

            contours, hierarchy = cv2.findContours(thresh_morp, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            # print("mkhb ==========================================")
            mkhb1_2 = None
            mkhb2_1 = None
            mkhb2_2 = None
            mkhb3_1 = None
            mkhb3_2 = None
            mkhb4_1 = None
            mkhb4_2 = None
            for cont in contours:
                area = cv2.contourArea(cont)
                epsilon = 0.01 * cv2.arcLength(cont, True)
                approx = cv2.approxPolyDP(cont, epsilon, True)
                if(area<200 and area>80 ):
                    a_sorted, box = get_sorted_box(approx)
                    if a_sorted is not None:
                    # print(a_sorted)
                        if  a_sorted[0][0] <150 :
                            mkhb1_2 = a_sorted[2][0]
                            # print(mkhb1_2)
                        elif a_sorted[0][0] >150 and a_sorted[0][0] <375 :
                            mkhb2_1 = a_sorted[0][0]
                            mkhb2_2 = a_sorted[2][0]
                            # print(mkhb2_1)
                            # print(mkhb2_2)
                        elif a_sorted[0][0] >375 and a_sorted[0][0] <575 :
                            mkhb3_1 = a_sorted[0][0]
                            mkhb3_2 = a_sorted[2][0]
                            # print(mkhb3_1)
                            # print(mkhb3_2)
                        elif a_sorted[0][0] >575 :
                            mkhb4_1 = a_sorted[0][0]
                            mkhb4_2 = a_sorted[2][0]
                            # print(mkhb4_1)
                            # print(mkhb4_2)
            if mkhb1_2 is None or mkhb2_1 is None or mkhb2_2 is None or mkhb3_1 is None or mkhb3_2 is None or mkhb4_1 is None or mkhb4_2 is None: error_mkhb = "can't find mkhb at "+filename

            mask = np.zeros(thresh.shape[:2], np.uint8)
            mask[height3-100:height3, 850:width3] = 255
            masked_img = cv2.bitwise_and(thresh,thresh,mask = mask)
            kernel = np.ones((8,8),np.uint8)
            thresh_morp = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)

            contours, hierarchy = cv2.findContours(thresh_morp, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

            # print("mkhb5 ==========================================")
            mkhb5_1 = None
            for cont in contours:
                area = cv2.contourArea(cont)
                epsilon = 0.01 * cv2.arcLength(cont, True)
                approx = cv2.approxPolyDP(cont, epsilon, True)
                if(area<200 and area>80 ):
                    a_sorted, box = get_sorted_box(approx)
                    if a_sorted is not None:
                        # print(a_sorted)
                        mkhb5_1 = (a_sorted[2][0] - a_sorted[0][0]) / 4.0
                        mkhb5_1 = int(round(mkhb5_1))
                        mkhb5_1 = a_sorted[0][0] + mkhb5_1

            gray = cv2.cvtColor(table_ans, cv2.COLOR_BGR2GRAY)
            # gray = cv2.GaussianBlur(gray, (5, 5), 0)
            ret, thresh = cv2.threshold(gray, threshold_ans, 255, cv2.THRESH_BINARY)
            # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            linek = np.ones((3, 3),np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, linek ,iterations=1)
            # cv2.imshow("0", thresh)
            # cv2.waitKey(0)

            if (error_mkv is None and 
                error_mkvr is None and 
                error_mkh is None and 
                error_mkhb is None):
                if mkv1 is not None and mkv2 is not None and mkv3 is not None and mkv4 is not None:
                    mkv  = [mkv1,mkv2,mkv3,mkv4]
                if mkvr1 is not None and mkvr2 is not None and mkvr3 is not None and mkvr4 is not None:
                    mkvr = [mkvr1,mkvr2,mkvr3,mkvr4]
                if mkh1_2 is not None and mkh2_1 is not None and mkh2_2 is not None and mkh3_1 is not None and mkh3_2 is not None and mkh4_1 is not None and mkh4_2 is not None:
                    mkh1 = [mkh1_2,mkh2_2,mkh3_2,mkh4_2]
                    mkh2 = [mkh2_1,mkh3_1,mkh4_1,mkh5_1]

                ans = []
                ans_format = ['A','B','C','D','E','F','G','H']
                n=0

                if num_choice%10!=0:
                    loop = num_choice/10 +1
                else:
                    loop = num_choice/10

                num_ch = 0
                count = 0
                for l in range(int(loop)):
                    spv = int(round((mkv[(l%3)+1] - mkv[l%3])/10.0))
                    mkvs = int(round(mkv[l%3] + spv/2.0))

                    l1 = int(l/3)
                    sph = int(round((mkh2[l1]-mkh1[l1] )/ 10.0))
                    mkhs = int(mkh1[l1]+sph)

                    for r in range(10):
                        num_ch += 1
                        for row in range(8):
                            mask = np.zeros(table_ans.shape[:2], np.uint8)
                            pixel_v = 5
                            pixel_h = 1

                            y_start = mkvs+(spv*r)+pixel_v
                            y_end = mkvs+spv+(spv*r)-pixel_v

                            x_start = mkhs+(sph*row)
                            x_end = mkhs+sph+(sph*row)-pixel_h

                            mask[y_start:y_end, x_start:x_end] = 255

                            true_pix, hist_mask = get_true_pix(thresh, mask)
                            if true_pix >= true_pix_check :
                                if n == 0 :
                                    ans.append([])
                                    ans[num_ch-1].append(num_ch)
                                    n+=1
                                ans[num_ch-1].append(ans_format[row])
                                count = count +1
                        if count == 0 :
                            ans.append([])
                            ans[num_ch-1].append(num_ch)
                            ans[num_ch-1].append("n")
                        count = 0
                        n=0
                        if num_choice == num_ch : break
                    if num_choice == num_ch : break
        
        if table_std is None : error_table_std = "ไม่พบตารางรหัสนักศึกษา"
        if table_sub is None : error_table_sub = "ไม่พบตารางรหัสวิชา"
        if table_ans is None or error_mkv is not None or error_mkvr is not None or error_mkh is not None or error_mkhb is not None: 
            error_table_ans = "ไม่พบ Marker ของส่วนคำตอบ"

        error = [error_table_std, error_table_sub, error_table_ans]
        ##############################################################################
        
        if (error_mkv is None and 
            error_mkvr is None and 
            error_mkh is None and 
            error_mkhb is None) and debug == True and table_ans is not None:
            num_ans = 0
            n=0

            if num_choice%10!=0:
                loop = num_choice/10 +1
            else:
                loop = num_choice/10

            num_ch = 0
            count = 0
            for l in range(int(loop)):
                spv = int(round((mkv[(l%3)+1] - mkv[l%3])/10.0))
                mkvs = int(round(mkv[l%3] + spv/2.0))

                l1 = int(l/3)
                sph = int(round((mkh2[l1]-mkh1[l1])/ 10.0))
                mkhs = int(mkh1[l1]+sph)
                
                for r in range(10):
                    num_ch += 1
                    for row in range(8):
                        mask = np.zeros(table_ans.shape[:2], np.uint8)
                        pixel_v = 5
                        pixel_h = 1

                        y_start = mkvs+(spv*r)+pixel_v
                        y_end = mkvs+spv+(spv*r)-pixel_v

                        x_start = mkhs+(sph*row)
                        x_end = mkhs+sph+(sph*row)-pixel_h

                        mask[y_start:y_end, x_start:x_end] = 255

                        true_pix, hist_mask = get_true_pix(thresh, mask)
                        if true_pix >= true_pix_check :
                            num_ans += 1
                            true_pix = np.around(true_pix,2)
                            cv2.putText(table_ans, str(true_pix[0]), (x_start,y_start-3), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,0,255), 1)
                            cv2.rectangle(table_ans,(x_start,y_start),(x_end,y_end),(0,0,255),1)
                            count = count +1
                        else :
                            true_pix = np.round(true_pix,2)
                            cv2.putText(table_ans, str(true_pix[0]), (x_start,y_start-3), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,0,255), 1)
                            cv2.rectangle(table_ans,(x_start,y_start),(x_end,y_end),(0,255,0),1)
                    count = 0
                    n=0
                    if num_choice == num_ch : break
                if num_choice == num_ch : break
            cv2.putText(table_ans, str(num_ans), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)

            isExist = os.path.exists(srcpath+"table_ans_detect/")
            if isExist == False:
                os.mkdir(srcpath+"table_ans_detect/")
            if table_ans is not None:
                cv2.imwrite(srcpath+"table_ans_detect/table_ans_"+filename, table_ans)
        
        ##############################################################################
        return (error, std_id, sec, seat_id, sub_id, ex_id, ans)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        err = "Process Ans Error Line "+str(exc_tb.tb_lineno if exc_tb else None)+" : "+str(e)+" at file: "+filename
        return ([err], 0, 0, 0, 0, 0, 0)

# if __name__ == '__main__':
#     img_list = []
#     for filename in glob.glob('image/original/result/*.jpg'):
#         filename = filename.split("\\")[1]
#         print(str(process_ans("image/original/result/", filename, 40)[0]))
#         print("=====================================================================================================")
