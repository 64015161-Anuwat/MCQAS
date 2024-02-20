# -*- coding: utf-8 -*-
import re
from pythainlp.tokenize import sent_tokenize
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys, os

def create_questionnaire_sheet(dstpath,head_1,detail1,detail2,part_1,part_2,qrcode=None,logo=None):
    try:
        path = os.getcwd()+"/api/image_process/assets/"
        error = ""

        height = 3507
        width = 2481
        margin = 50
        bg = (255,255,255)
        black = (0,0,0)
        white = (255,255,255)
        gray = (192,192,192)
        cirtext = (70,70,70)

        fonttext = ImageFont.truetype(path+'_arisa.ttf',70)
        fonttext1 = ImageFont.truetype(path+'_arisa.ttf',35)
        fonttext1_2 = ImageFont.truetype(path+'_arisa.ttf',32)
        fonttext2 = ImageFont.truetype(path+'_arisa.ttf',60)
        fonttext3 = ImageFont.truetype(path+'_arisa.ttf',45)
        fonttext5 = ImageFont.truetype(path+'_arisa.ttf',50)
        fonttext4 = ImageFont.truetype(path+'_arisa.ttf',65)
        fo =  ImageFont.truetype(path+'newDB.ttf',70)
        fo1 = ImageFont.truetype(path+'newDB.ttf',60)


        img = np.zeros((height,width,3), np.uint8)
        img[:,:] = bg
        cv2.rectangle(img,(margin,margin),(width-margin,height-margin),black,3)
        logo_ = cv2.imread(path+"logo.jpg")
        logo_ = cv2.resize(logo_,(300,135))
        x_offset=2000
        y_offset=60
        img [y_offset:y_offset+logo_.shape[0], x_offset:x_offset+logo_.shape[1]]=logo_

        if logo != None:
            logo = cv2.imread(logo)
            logo = cv2.resize(logo,(300,135))
            x_offset=180
            y_offset=60
            img [y_offset:y_offset+logo.shape[0], x_offset:x_offset+logo.shape[1]]=logo

        if qrcode == None:
            QR = cv2.imread(path+"qrcode.jpg")
        else:
            QR = cv2.imread(qrcode)

        # QR = cv2.resize(QR,(80,80))
        # QR = cv2.resize(QR,(100,100))
        # QR = cv2.resize(QR,(120,120))
        QR = cv2.resize(QR, (200, 200))
        ####### no border
        # x_offset=2349
        # x_offset=2329
        # x_offset=2309
        x_offset=2225
        # y_offset=53
        y_offset=3250
        ####### border
        # x_offset=2351
        # x_offset=2331
        # x_offset=2311
        # y_offset=51
        img [y_offset:y_offset+QR.shape[0], x_offset:x_offset+QR.shape[1]]=QR

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)

        ########## head
        head1 = head_1
        
        limitleft = 500
        limitright = 1830
        limitleft = 50
        limitright = 2431
        head_1 = head1
        detail1 = detail1
        detail2 = detail2
        fonthead = ImageFont.truetype(path+'newDB.ttf',60)
        if 1240-(fo.font.getsize(head_1)[0][0] /2 ) < limitleft or (1240 - (fo.font.getsize(head_1)[0][0] /2 )) + (fo.font.getsize(head_1)[0][0] ) > limitright:
            error += "Too long head name\n"
        else:
            draw.text((1240 - (fo.font.getsize(head_1)[0][0] /2 ),130),head_1,black, font=fonthead)
        if 1240-(fonttext2.font.getsize(detail1)[0][0] /2 ) < limitleft or (1240 - (fonttext2.font.getsize(detail1)[0][0] /2 )) + (fonttext2.font.getsize(detail1)[0][0] ) > limitright:
            error += "Too long detail1\n"
        else:
            draw.text((1240 - (fonttext2.font.getsize(detail1)[0][0] /2 ),210),detail1,black, font=fonttext2)
        if 1240-(fonttext2.font.getsize(detail2)[0][0] /2 ) < limitleft or (1240 - (fonttext2.font.getsize(detail2)[0][0] /2 )) + (fonttext2.font.getsize(detail2)[0][0] ) > limitright:
            error += "Too long detail2\n"
        else:
            draw.text((1240 - (fonttext2.font.getsize(detail2)[0][0] /2 ),310),detail2,black, font=fonttext2)


        draw.text((150,450), "คำชี้แจง",black, font=fo1)
        draw.text((310,425), "กรุณาระบายวงกลมในช่องที่ท่านต้องการลงในแบบสอบถาม",black, font=fonttext2)


        ########## part 1
        # part1 = [[str0_0,str0_1 ,str0_2,str0_3,str0_4],
        #          [str1_0,str1_1,str1_2,str1_3,str1_4],
        #          [str2_0,str2_1,str2_2,str2_3,str2_4],
        #          [str3_0,str3_1,str3_2,str3_3,str3_4],
        #          [str4_0,str4_1,str4_2,str4_3,str4_4]]
        part1 = part_1

        draw.text((150,525), "ส่วนที่ 1",black, font=fo1)
        draw.text((310,500), "ข้อมูลทั่วไป",black, font=fonttext2)

        ########## information
        space = 0
        for index_t1,t1 in enumerate(part1):
            
            for index_t2,t2 in enumerate(t1):

                result = str(t2)+" "
                if index_t2 == 0:
                    space = 200
                    draw.text((space,640+(100*index_t1)), result, black, font=fo1)
                elif index_t2 == 1:
                    space = 200+621
                    draw.text((space,615+(100*index_t1)), result, black, font=fonttext2)
                else:
                    space += 400
                    draw.text((space,615+(100*index_t1)), result, black, font=fonttext2)

        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        cv2.rectangle(img,(150,600),(width-150,1100),black,5)

        ########### circle
        for index_pt1,pt1 in enumerate(part1):
            for index_pt2,pt2 in enumerate(pt1):
                if pt2 != '':
                    if index_pt2!=0 :
                        cv2.circle(img,(751+(400*(index_pt2-1)),650+(100*index_pt1)),16,cirtext,1)
                        cv2.putText(img,str(index_pt2),(742+(400*(index_pt2-1)),660+(100*index_pt1)),cv2.FONT_HERSHEY_SIMPLEX,0.9,cirtext,1)




        ########## part2
        # part2 = [[hd1_1,str0,str1,str2],
        #          [hd1_2,str3,str4,str5,str6,str7,str8],
        #          [hd1_3,str9,str10,str11,str12,str13]]
        part2 = part_2

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)

        draw.text((150,1145), "ส่วนที่ 2",black, font=fo1)
        draw.text((310,1120), "ความคิดเห็นเกี่ยวกับแบบสอบถาม (5 = มากที่สุด, 4 = มาก, 3 = ปานกลาง, 2 = น้อย, 1 = น้อยที่สุด, 0 = ไม่ประเมิน)",black, font=fonttext2)
        draw.text((900,1230), "หัวข้อ",black, font=fonttext)
        draw.text((1920,1225), "ระดับความคิดเห็น",black, font=fonttext3)
        draw.text((1745,1300), "มากที่สุด",black, font=fonttext1)
        draw.text((1865,1300), "มาก",black, font=fonttext1)
        draw.text((1937,1300), "ปานกลาง",black, font=fonttext1)
        draw.text((2065,1300), "น้อย",black, font=fonttext1)
        draw.text((2142,1300), "น้อยที่สุด",black, font=fonttext1)
        draw.text((2228,1300), " ไม่ประเมิน",black, font=fonttext1_2)

        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        c1=0
        for i in part2:
            for index_j,j in enumerate(i):
                if index_j!=0:
                    if j != '':
                        for ch1 in range(6):
                            cv2.circle(img,(1781+(100*ch1),1398+(98*(c1))),16,cirtext,1)
                            cv2.putText(img,str(ch1),(2272-(100*ch1),1408+(98*(c1))),cv2.FONT_HERSHEY_SIMPLEX,0.9,cirtext,1)
                    c1+=1
                else:
                    if j != "Nohead":
                        cv2.rectangle(img,(150,1350+(98*c1)),(2331,1448+(98*c1)),gray,-1)
                        c1+=1

        cv2.rectangle(img,(150,1210),(width-150,3114),black,2)
        cv2.line(img,(1731,1280),(width-150,1280),black,2)
        cv2.rectangle(img,(1731,1350),(width-150,3114),black,5)

        for line1 in range(18):
            cv2.line(img,(150,1350+(98*line1)),(width-150,1350+(98*line1)),black,2)

        for cl in range(6):
            if cl == 0:
                ln = 1210
            else:
                ln = 1280
            cv2.line(img,(1731+(100*cl),ln),(1731+(100*cl),3114),black,2)


        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)


        c=0
        c0=0
        c1=0
        c2=0
        o=0
        count=0
        fonth1_size = 60
        fontsh1_size = 55
        if45 = 0

        for i in part2:
            csub = 1
            for ch0 in range(len(part2[c0])):
                if ch0 == 0 :
                    if part2[c0][ch0] != "Nohead" and part2[c0][ch0] != "":
                        word = part2[c0][ch0]
                        word = str(word)
                        fonth1 = ImageFont.truetype(path+'newDB.ttf',fonth1_size)
                        b1 = ""
                        b2 = ""
                        while int(fonth1.font.getsize(word)[0][0]) > 1550 :
                            if fonth1_size <= 45:
                                if45 = 1
                                sp = [i for i in range(len(word)) if word.startswith(" ", i)]
                                b1 = word
                                word=word.replace(" ", "")
                                print(word)
                                a=sent_tokenize(word)
                                print(a)
                                n=len(a)
                                while fonth1.font.getsize(b1)[0][0] > 1550 :
                                    b1="".join(a[0:n])
                                    n-=1
                                    for z in sp:
                                        if z < len(b1):
                                            b1 = b1[:z]+" "+b1[z:]

                                b2 = "".join(a[n+1:len(a)])
                                for z in sp:
                                        if z < len(b1)+len(b2) and z > len(b1):
                                            b2 = b2[:z-len(b1)]+" "+b2[z-len(b1):]
                                b1+=" "
                                b2+=" "
                                break
                            if if45 == 0:
                                fonth1_size -=1
                                fonth1 = ImageFont.truetype(path+'newDB.ttf',fonth1_size)

                        if if45 > 0:
                            draw.text((175,1353+18+(98*c1)),b1,black, font=fonth1)
                            draw.text((175,1396+18+(98*c1)),b2,black, font=fonth1)
                            if45 = 0
                        else:
                            word+=" "
                            draw.text((175,1370+18+(98*c1)),word,black, font=fonth1)
                        fonth1_size = 60
                        c1+=1
                else:
                    if part2[c0][ch0] != "":
                        word = part2[c0][ch0]
                        word = str(word)
                        fontsh1 = ImageFont.truetype(path+'_arisa.ttf',fontsh1_size)
                        b1 = ""
                        b2 = ""
                        while int(fontsh1.font.getsize(word)[0][0]) > 1500 :
                            if fontsh1_size <= 45:
                                if45 = 1
                                if len(part2) == 1:
                                    ch0+=1
                                sp = [i for i in range(len(word)) if word.startswith(" ", i)]
                                b1 = word
                                word=word.replace(" ", "")
                                a=sent_tokenize(word)
                                n=len(a)
                                while fontsh1.font.getsize(b1)[0][0] > 1500 :
                                    b1="".join(a[0:n])
                                    n-=1
                                    for z in sp:
                                        if z < len(b1):
                                            b1 = b1[:z]+" "+b1[z:]

                                b2 = "".join(a[n+1:len(a)])
                                for z in sp:
                                        if z < len(b1)+len(b2) and z > len(b1):
                                            b2 = b2[:z-len(b1)]+" "+b2[z-len(b1):]
                                b1+=" "
                                b2+=" "
                                break
                            if if45 == 0:
                                fontsh1_size -=1
                                fontsh1 = ImageFont.truetype(path+'_arisa.ttf',fontsh1_size)

                        if if45 > 0:
                            draw.text((170,1353+(98*c1)),str(ch0)+". "+b1,black, font=fontsh1)
                            draw.text((210,1396+(98*c1)),b2,black, font=fontsh1)
                            if45 = 0
                        else:
                            word+=" "
                            if len(part2) ==1:
                                ch0+=1
                            draw.text((170,1370+(98*c1)),str(csub)+". "+word,black, font=fontsh1)
                            csub+=1
                        fontsh1_size = 55	
                        c1+=1
            c0+=1

        ########## part3

        draw.text((150,3175), "ส่วนที่ 3",black, font=fo1)
        draw.text((310,3150), "ข้อเสนอแนะเพิ่มเติม เพื่อการปรับปรุงแก้ไขครั้งต่อไป",black, font=fonttext2)

        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        parttree = 150
        for line2 in range(2):
            cv2.line(img,(parttree,3290+(100*line2)),(width-parttree-200,3290+(100*line2)),(0,0,0),2)

        if(error == ""):
            cv2.imwrite(dstpath+"questionnaire_sheet.jpg", img)
            return True
            
        else:
            return error
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if exc_tb is not None:
            return "Error Line " + str(exc_tb.tb_lineno) + " : " + str(e)
        else:
            return "Error: " + str(e)

# if __name__ == '__main__':
#     r = re.compile("ี|ิ|ึ|ื|ั|่|้|๊|๋|็|์|ํ|ฺ|ฺ|ฺ|ํ|ฺ")
    
    
#     dstpath = ""
#     head_1 = "กกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกก" # manx 60
#     detail1 = "" # max 95
#     detail2 = "หลังเข้ารับการอบรม ท่านมีความรู้ความเข้าใจหลังการฝึกอบรม" # max 95
#     part_1 = [["กกกกกกกกกกกกกกกกกกกก", "กกกกกกกกกกกก", "หญิง"],  # 20 15
#               ["ระดับชั้น", "ม.4", "ม.5", "ม.6", "อื่นๆ______"], 
#               ["สถานศึกษา", "โรงเรียน", "อบจ.", "อื่นๆ______"],
#               ["สถานที่อบรม", "โรงเรียน", "อบจ.", "อื่นๆ______"], 
#               ["ประเภทการอบรม", "อบรม", "สัมมนา", "อื่นๆ______"]]
#     part_2 = [["กกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกก","กกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกกก","วิธีถ่ายทอดเนื้อหาน่าสนใจ","เอกสาร/สื่อ ประกอบการบรรยาย","การตอบคำถามตรงประเด็น","ความเหมาะสมของวิทยากรโดยรวม"],
#               ["การรับข่าวประชาสัมพันธ์การจัดอมรม","การประสานงานการต้อนรับ","ระยะเวลาการอมรม","ความพร้อมอุปกรณ์/สื่ออิเล็กทรอนิกส์ต่างๆ","ความเหมาะสมของสถานที่"]] # 100
#     new_s = r.sub("",part_2[0][1])
#     print(new_s)
#     print(len(new_s))
#     print(create_questionnaire_sheet(dstpath,head_1,detail1,detail2,part_1,part_2,logo=os.getcwd()+"/api/image_process/assets/logo.jpg"))