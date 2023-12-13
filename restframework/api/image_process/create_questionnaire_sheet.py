# -*- coding: utf-8 -*-
import re
from re import T
import pythainlp as pythai
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys, os

def createinfsheet(dstpath,head_1,detail1,detail2,part_1,part_2):
    try:
        height = 3507
        width = 2481
        margin = 50
        bg = (255,255,255)
        black = (0,0,0)
        white = (255,255,255)
        gray = (192,192,192)
        cirtext = (70,70,70)

        fonttext = ImageFont.truetype('other/_arisa.ttf',70)
        fonttext1 = ImageFont.truetype('other/_arisa.ttf',35)
        fonttext1_2 = ImageFont.truetype('other/_arisa.ttf',32)
        fonttext2 = ImageFont.truetype('other/_arisa.ttf',60)
        fonttext3 = ImageFont.truetype('other/_arisa.ttf',45)
        fonttext5 = ImageFont.truetype('other/_arisa.ttf',50)
        fonttext4 = ImageFont.truetype('other/_arisa.ttf',65)
        fo =  ImageFont.truetype('other/newDB.ttf',70)
        fo1 = ImageFont.truetype('other/newDB.ttf',60)


        img = np.zeros((height,width,3), np.uint8)
        img[:,:] = bg
        cv2.rectangle(img,(margin,margin),(width-margin,height-margin),black,3)
        logo = cv2.imread("other/logo.jpg")
        logo = cv2.resize(logo,(300,135))
        x_offset=2000
        y_offset=60
        img [y_offset:y_offset+logo.shape[0], x_offset:x_offset+logo.shape[1]]=logo

        QR = cv2.imread("other/qrcode.jpg")
        QR = cv2.resize(QR,(80,80))
        x_offset=2351
        y_offset=51
        img [y_offset:y_offset+QR.shape[0], x_offset:x_offset+QR.shape[1]]=QR

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)

        #head
        head1 = head_1
        # draw.text((1130,130), "แบบสอบถาม",black, font=fo)
        
        limitleft = 150
        limitright = 2330
        head_1 = head1
        detail1 = detail1
        detail2 = detail2
        fonthead = ImageFont.truetype('other/newDB.ttf',60)
        if 1240-(fo.font.getsize(head_1)[0][0] /2 ) < limitleft or (1240 - (fo.font.getsize(head_1)[0][0] /2 )) + (fo.font.getsize(head_1)[0][0] ) > limitright:
            return "Too long head name"
        else:
            draw.text((1240 - (fo.font.getsize(head_1)[0][0] /2 ),130),head_1,black, font=fonthead)
        if 1240-(fonttext2.font.getsize(detail1)[0][0] /2 ) < limitleft or (1240 - (fonttext2.font.getsize(detail1)[0][0] /2 )) + (fonttext2.font.getsize(detail1)[0][0] ) > limitright:
            return "Too long detail1"
        else:
            draw.text((1240 - (fonttext2.font.getsize(detail1)[0][0] /2 ),210),detail1,black, font=fonttext2)
        if 1240-(fonttext2.font.getsize(detail2)[0][0] /2 ) < limitleft or (1240 - (fonttext2.font.getsize(detail2)[0][0] /2 )) + (fonttext2.font.getsize(detail2)[0][0] ) > limitright:
            return "Too long detail2"
        else:
            draw.text((1240 - (fonttext2.font.getsize(detail2)[0][0] /2 ),310),detail2,black, font=fonttext2)


        draw.text((150,450), "คำชี้แจง",black, font=fo1)
        draw.text((310,425), "กรุณาระบายวงกลมในช่องที่ท่านต้องการลงในแบบสอบถาม",black, font=fonttext2)


        #####################part 1

        # str0_0 = "เพศ"
        # str0_1 = "ชาย"
        # str0_2 = "หญิง"
        # str0_3 = ""
        # str0_4 = ""

        # str1_0 = "สถานภาพ"
        # str1_1 = "นักเรียน"
        # str1_2 = "บุคคลทั่วไป"
        # str1_3 = ""
        # str1_4 = ""

        # str2_0 = "ระดับชั้น"
        # str2_1 = "ม.4"
        # str2_2 = "ม.5"
        # str2_3 = "ม.6"
        # str2_4 = "อื่นๆ _____________"

        # str3_0 = "อบรมความรู้ด้าน"
        # str3_1 = "Network"
        # str3_2 = "Robot"
        # str3_3 = ""
        # str3_4 = ""

        # str4_0 = "จำนวนบุตร"
        # str4_1 = "1 คน"
        # str4_2 = "2 คน"
        # str4_3 = "3 คน"
        # str4_4 = "มากกว่านั้น"

        # part1 = [[str0_0,str0_1 ,str0_2,str0_3,str0_4],
        #          [str1_0,str1_1,str1_2,str1_3,str1_4],
        #          [str2_0,str2_1,str2_2,str2_3,str2_4],
        #          [str3_0,str3_1,str3_2,str3_3,str3_4],
        #          [str4_0,str4_1,str4_2,str4_3,str4_4]]
        part1 = part_1

        draw.text((150,525), "ส่วนที่ 1",black, font=fo1)
        draw.text((310,500), "ข้อมูลทั่วไป",black, font=fonttext2)

        #information
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
                
                # draw.text((space,615+(100*index_t1)), result,black, font=fonttext5)

        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        cv2.rectangle(img,(150,600),(width-150,1100),black,5)
        #circle
        for index_pt1,pt1 in enumerate(part1):
            for index_pt2,pt2 in enumerate(pt1):
                if index_pt2!=0 :
                    cv2.circle(img,(751+(400*(index_pt2-1)),650+(100*index_pt1)),16,cirtext,1)
                    cv2.putText(img,str(index_pt2),(742+(400*(index_pt2-1)),660+(100*index_pt1)),cv2.FONT_HERSHEY_SIMPLEX,0.9,cirtext,1)




        #####################part2

        # hd1_1 = "ความรู้ความเข้าใจของผู้ได้รับการอบรมความรู้ความเข้าใจของผู้ได้รับการอบรมการอบรมการอบรมการอบความรู้ความเข้าใจของผู้ได้รับการอบรมความรู้ความเข้าใจของ"
        # hd1_2 = "ความรู้ความเข้าใจของผู้ได้รับการอบรมความรู้ความเข้าใจของผู้ได้รับการอบรมการอบรมการอบรมการอบรม"

        # str0 = "ถ้าหากรักนี้ไม่บอก ไม่พูดไม่กล่าว แล้วเค้าจะรู้ว่ารักหรือป่าว อาจจะไม่แน่ใจ อยากให้เค้ารู้เธอคงต้องแสดงออก ไม่ใช่ให้ใครมา"
        # str1 = "พึ่งจะมองตัวเองแต่ก่อนเคยละเลย ลืมว่าเคยมีเธอความรักเลยเลือนลาง กว่าจะรู้สำนึกจะบอกว่ารักแต่มันก็สาย สายเกินคงสายไป แต่หัวใจ ฉันนั้นมันยังไม่ลืมว่ารักเธอ"
        # str2 = "คนเดินถนนคนนึงมันจะทำเธอซึ้งและเป็นสุขได้สักเท่าไหร่ แค่เพียงดอกไม้ริมทาง เธอจะมองมันสวยถึงเมื่อไหร่กัน"
        # str3 = "การเกินทางของฉันและเธอคือการเรียนรู้ การเรียนรู้ของเราสองคนคือความเข้าใจ เธอเข้าใจและฉันเข้าใจก็ทำให้เรามั่นใจ"
        # str4 = "สุดท้ายแล้วเราจะเป็นคนรักหรือเป็นแค่คนรู้จัก ช่วยบอกสักครั้ง บอกให้ฉันหยุดทรมาร"
        # str5 = "ไม่มีสิทธิ์ที่จะไปห้ามให้เธอ ไม่ไป ในเมื่อเธอไม่เหลือใจ ห้ามทำไม ได้แต่บอกและสั่งตัวเองให้คอยห้ามใจ"
        # str6 = "ไม่ให้เธอไป ต้องเสียอะไร แค่ไหนอะไรยังไง ฉันจะไป บอกฉันสักคำแค่ไหนที่เธอต้องการ โดยปกติแล้วการทำการบ้าน"
        # str7 = "เปลี่ยนได้ไหมขอเป็นคนที่โดนทอดทิ้งทุกรอยช้ำทุกอย่าง ที่เค้ารังแกบอกเลยยอมทั้งนั้นแม้ถ่อยคำที่ฟังแล้วช้ำร้ายแรงสักเท่าไหร่ที่เขาทำเธอ ขอเจ็บแทน"
        # str8 = "พึ่งจะมองตัวเองแต่ก่อนเคยละเลย ลืมว่าเคยมีเธอความรักเลยเลือนลาง กว่าจะรู้สำนึกจะบอกว่ารักแต่มันก็สาย สายเกินคงสายไป แต่หัวใจ ฉันนั้นมันยังไม่ลืมว่ารักเธอ"
        # str9 = "คนเดินถนนคนนึงมันจะทำเธอซึ้งและเป็นสุขได้สักเท่าไหร่ แค่เพียงดอกไม้ริมทาง เธอจะมองมันสวยถึงเมื่อไหร่กัน"
        # str10 = "การเกินทางของฉันและเธอคือการเรียนรู้ การเรียนรู้ของเราสองคนคือความเข้าใจ เธอเข้าใจและฉันเข้าใจก็ทำให้เรามั่นใจ"
        # str11 = "สุดท้ายแล้วเราจะเป็นคนรักหรือเป็นแค่คนรู้จัก ช่วยบอกสักครั้ง บอกให้ฉันหยุดทรมาร"
        # str12 = "ไม่มีสิทธิ์ที่จะไปห้ามให้เธอ ไม่ไป ในเมื่อเธอไม่เหลือใจ ห้ามทำไม ได้แต่บอกและสั่งตัวเองให้คอยห้ามใจ"
        # str13 = "ไม่ให้เธอไป ต้องเสียอะไร แค่ไหนอะไรยังไง ฉันจะไป บอกฉันสักคำแค่ไหนที่เธอต้องการ โดยปกติแล้ว การทำการบ้าน"
        # str14 = "ได้ไหมขอเป็นคนที่โดนทอดทิ้งทุกรอยช้ำทุกอย่าง ที่เค้ารังแกบอกเลยยอมทั้งนั้นแม้ถ่อยคำที่ฟังแล้วช้ำร้ายแรงสักเท่าไหร่ที่เขาทำเธอ ขอเจ็บแทน"
        # str15 = "ไม่มีสิทธิ์ที่จะไปห้ามให้เธอ ไม่ไป ในเมื่อเธอไม่เหลือใจ ห้ามทำไม ได้แต่บอกและสั่งตัวเองให้คอยห้ามใจ"
        # str16 = "ไม่ให้เธอไป ต้องเสียอะไร แค่ไหนอะไรยังไง ฉันจะไป บอกฉันสักคำแค่ไหนที่เธอต้องการ โดยปกติแล้ว การทำการบ้าน"
        # str17 = "ได้ไหมขอเป็นคนที่โดนทอดทิ้งทุกรอยช้ำทุกอย่าง ที่เค้ารังแกบอกเลยยอมทั้งนั้นแม้ถ่อยคำที่ฟังแล้วช้ำร้ายแรงสักเท่าไหร่ที่เขาทำเธอ ขอเจ็บแทน"

        # hd1_1 = "ความรู้ความเข้าใจของผู้ได้รับการอบรม"
        # str0 = "ก่อนเข้ารับการอบรม ท่านมีความรู้ความเข้าใจก่อนการฝึกอบรม"
        # str1="หลังเข้ารับการอบรม ท่านมีความรู้ความเข้าใจหลังการฝึกอบรม"
        # str2="ประโยชน์จากการนำความรู้ความเข้าใจที่ได้จากการฝึกอบรม"
        # hd1_2="วิทยากร"
        # str3="ความรู้เกี่ยวกับหัวข้อหลังการบรรยาย"
        # str4="การบรรยายชัดเจนเข้าใจง่าย"
        # str5="วิธีถ่ายทอดเนื้อหาน่าสนใจ"
        # str6="เอกสาร/สื่อ ประกอบการบรรยาย"
        # str7="การตอบคำถามตรงประเด็น"
        # str8="ความเหมาะสมของวิทยากรโดยรวม"
        # hd1_3="รูปแบบการดำเนินการ"
        # str9="การรับข่าวประชาสัมพันธ์การจัดอมรม"
        # str10="การประสานงานการต้อนรับ"
        # str11="ระยะเวลาการอมรม"
        # str12="ความพร้อมอุปกรณ์/สื่ออิเล็กทรอนิกส์ต่างๆ"
        # str13="ความเหมาะสมของสถานที่"
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
                    if part2[c0][ch0] != "Nohead":
                        word = part2[c0][ch0]
                        word = str(word)
                        fonth1 = ImageFont.truetype('other/newDB.ttf',fonth1_size)
                        while int(fonth1.font.getsize(word)[0][0]) > 1550 :
                            if fonth1_size <= 45:
                                if45 = 1
                                sp = [i for i in range(len(word)) if word.startswith(" ", i)]
                                b1 = word
                                word=word.replace(" ", "")
                                print(word)
                                a=pythai.split(word)
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
                                fonth1 = ImageFont.truetype('other/newDB.ttf',fonth1_size)

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
                    word = part2[c0][ch0]
                    word = str(word)
                    fontsh1 = ImageFont.truetype('other/_arisa.ttf',fontsh1_size)
                    while int(fontsh1.font.getsize(word)[0][0]) > 1500 :
                        if fontsh1_size <= 45:
                            if45 = 1
                            if len(part2) == 1:
                                ch0+=1
                            sp = [i for i in range(len(word)) if word.startswith(" ", i)]
                            b1 = word
                            word=word.replace(" ", "")
                            a=pythai.split(word)
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
                            fontsh1 = ImageFont.truetype('other/_arisa.ttf',fontsh1_size)

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

           #     if len(part2[c0][0])/3 > limit :
                #
                #         sp = [i for i in range(len(word)) if word.startswith(" ", i)]
                #         for g in range(len(sp)):
                #             if limit>sp[g]:
                #                o=g
                #
                #         word=word.replace(" ", "")
                #         a=pythai.split(word)
                #         for n in range(len(a)):
                #             c+=len(a[n])
                #             if c+len(sp[0:o])>= limit:
                #                 b=word[c-len(a[n]):len(word)]
                #                 a=word[0:c-len(a[n])]
                #                 a+=" "
                #                 b+=" "
                #                 c=0
                #                 for z in sp:
                #                     if z > len(a):
                #                          b = b[:z-len(a)+1]+" "+b[z-len(a)+1:]
                #                     else:
                #                          a = a[:z]+" "+a[z:]
                #                 break
                #
                #         draw.text((175,1353+18+(98*c1)),a,black, font=fo2)
                #         draw.text((175,1396+18+(98*c1)),b,black, font=fo2)
                #     else:
                #         draw.text((175,1370+18+(98*c1)),word,black, font=fo1_2)
                # else:
                #     word = part2[c0][ch0]
                #     if len(part2[c0][ch0])/3 > limit :
                #         if len(part2) == 1:
                #             ch0+=1
                #
                #         sp = [i for i in range(len(word)) if word.startswith(" ", i)]
                #         for g in range(len(sp)):
                #             if limit>sp[g]:
                #                o=g
                #         word=word.replace(" ", "")
                #         a=pythai.split(word)
                #         for n in range(len(a)):
                #             c+=len(a[n])
                #             if c+len(sp[0:o])>= limit:
                #                 b=word[c-len(a[n]):len(word)]
                #                 a=word[0:c-len(a[n])]
                #                 a+=" "
                #                 b+=" "
                #                 c=0
                #                 for z in sp:
                #                     if z > len(a):
                #                          b = b[:z-len(a)+1]+" "+b[z-len(a)+1:]
                #                     else:
                #                          a = a[:z]+" "+a[z:]
                #                 break
                #
                #         draw.text((175,1353+(98*c1)),str(ch0)+". "+a,black, font=fonttext3)
                #         draw.text((210,1396+(98*c1)),b,black, font=fonttext3)
                #     else:
                #         if len(part2) ==1:
                #             ch0+=1
                #         draw.text((175,1370+(98*c1)),str(ch0)+". "+word,black, font=new)

        #####################part3

        draw.text((150,3175), "ส่วนที่ 3",black, font=fo1)
        draw.text((310,3150), "ข้อเสนอแนะเพิ่มเติม เพื่อการปรับปรุงแก้ไขครั้งต่อไป",black, font=fonttext2)

        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        parttree = 150
        for line2 in range(2):
            cv2.line(img,(parttree,3290+(100*line2)),(width-parttree,3290+(100*line2)),(0,0,0),2)



        # cv2.rectangle(img,(margin,margin),(width-margin,height-margin),black,3)
        #
        # logo = cv2.imread("logo.jpg")
        # logo = cv2.resize(logo,(300,135))
        # x_offset=2000
        # y_offset=60
        # img [y_offset:y_offset+logo.shape[0], x_offset:x_offset+logo.shape[1]]=logo
        #
        # QR = cv2.imread("qrcode.jpg")
        # QR = cv2.resize(QR,(80,80))
        # x_offset=2351
        # y_offset=51
        # img [y_offset:y_offset+QR.shape[0], x_offset:x_offset+QR.shape[1]]=QR
        #
        # #part 1
        # cv2.rectangle(img,(150,600),(width-150,1100),black,5)
        #

        #
        #
        # #part 2
        # cv2.rectangle(img,(150,1210),(width-150,3114),black,2)
        # cv2.rectangle(img,(150,1350),(2331,1448),gray,-1)
        # cv2.rectangle(img,(150,2232),(2331,2330),gray,-1)
        # cv2.line(img,(1731,1280),(width-150,1280),black,2)
        #
        # for line1 in range(18):
        #     cv2.line(img,(150,1350+(98*line1)),(width-150,1350+(98*line1)),black,2)
        #
        # cv2.line(img,(1731,1210),(1731,2710),black,2)
        #
        # for cl in range(6):
        #     cv2.line(img,(1731+(100*cl),1280),(1731+(100*cl),3114),black,2)
        #
        # for ch0 in range(1,18,1):
        #     for ch1 in range(6):
        #         if ch0 != 9:
        #             cv2.circle(img,(1780+(100*ch1),1400+(98*(ch0))),16,black,1)
        #             cv2.putText(img,str(ch1),(2272-(100*ch1),1408+(98*(ch0))),cv2.FONT_HERSHEY_COMPLEX,0.7,gray,1)
        #
        #
        #
        #
        # #part3
        # parttree = 150
        # for line2 in range(2):
        #     cv2.line(img,(parttree,3290+(100*line2)),(width-parttree,3290+(100*line2)),(0,0,0),2)
        #
        # #marker
        # cv2.rectangle(img,(1731,1350),(width-150,3114),black,5)
        #
        #
        #
        # #information
        # for i in range(5):
        #     for j in range(5):
        #          draw.text((200+(435*j),655+(85*i)), part1[i][j],black, font=fonttext3)
        #
        #
        # draw.text((150,1145), "ส่วนที่ 2",black, font=fo1)
        #
        # draw.text((310,1120), "ความคิดเห็นเกี่ยวกับการจัดทำโครงการ",black, font=fonttext2)
        # draw.text((900,1230), "หัวข้อ",black, font=fonttext)
        # draw.text((1920,1225), "ระดับความคิดเห็น",black, font=fonttext3)
        # draw.text((1750,1300), "มากที่สุด",black, font=fonttext1)
        # draw.text((1860,1300), "มาก",black, font=fonttext1)
        # draw.text((1945,1300), "ปานกลาง",black, font=fonttext1)
        # draw.text((2065,1300), "น้อย",black, font=fonttext1)
        # draw.text((2145,1300), "น้อยที่สุด",black, font=fonttext1)
        # draw.text((2245,1300), "ไม่ประเมิน",black, font=fonttext1)
        #
        # #draw.text((170,1395), list,black, font=fo1)
        #
        #
        # br = len(part2[0])+len(part2[1])
        # limit = 105
        # num = "-"
        # for i in range(len(part2)):
        #     if i==0:
        #         for j in range(len(part2[i])):
        #             if len(part2[i][j])>limit:
        #                 if part2[i][j]!=part2[0][0]:
        #                    draw.text((175,1353+(98*j)),part2[i][j][0:limit],black, font=fonttext3)
        #                     cv2.circle(img,(1780+(100*j),1400+(98*(i))),16,black,1)
        #                     cv2.putText(img,str(j),(2272-(100*j),1408+(98*(i))),cv2.FONT_HERSHEY_COMPLEX,0.7,gray,1)
        #
        #             if len(part2[i][j])<=limit:
        #                 if part2[i][j]!=part2[0][0]:
        #                     draw.text((175,1375+(98*j)),part2[i][j], black, font=new)
        #                 else:
        #                     draw.text((175,1385+(98*j)),part2[i][j], black, font=fo1)
        #             # print j
        #
        #     else :
        #         for k in range(len(part2[0]),18,1):
        #             if len(part2[i][k-(j+1)])>limit:
        #                 draw.text((175,1353+(98*k)),part2[i][k-(j+1)][0:limit],black, font=fonttext3)
        #                 draw.text((200,1396+(98*k)),part2[i][k-(j+1)][limit:200],black, font=fonttext3)
        #             if len(part2[i][k-(j+1)])<=limit:
        #                 if part2[i][k-(j+1)]!=part2[1][0]:
        #                     draw.text((175,1375+(98*k)),part2[i][k-(j+1)], black, font=new)
        #                     print "gfdsagdfsg"
        #                 else:
        #                     draw.text((175,1385+(98*k)),part2[i][k-(j+1)], black, font=fo1)
        #
        #             # print k
        #
        #
        #
        # draw.text((150,3175), "ส่วนที่ 3",black, font=fo1)
        # draw.text((310,3150), "ข้อเสนอแนะเพิ่มเติม เพื่อการปรับปรุงแก้ไขครั้งต่อไป",black, font=fonttext2)
        # #http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
        # img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        # #reimg = cv2.resize(img(1052,744))
        cv2.imwrite(dstpath+"infsheet.jpg",img)
        return True
        # cv2.imshow('image',img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # ans = []
        # ans.append([])
        # ans[0].append("เพศ")
        # ans[0].append("ชาย")
        # ans[0].append("หญิง")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        return "Error Line "+str(exc_tb.tb_lineno)+" : "+str(e)

# if __name__ == '__main__':
#     r = re.compile("ี|ิ|ึ|ื|ั|่|้|๊|๋|็|์|ํ|ฺ|ฺ|ฺ|ํ|ฺ")
#     string = "กี่จำไฟฟ้ามืดต์ฟํห๊"
#     new_s = r.sub("",string)
#     print(new_s)
#     print(len(new_s))
    
#     dstpath = ""
#     head_1 = "ความรู้ความเข้าใจก่อนการฝึกอบรม"
#     detail1 = "ก่อนเข้ารับการอบรม ท่านมีความรู้ความเข้าใจก่อนการฝึกอบรม"
#     detail2 = "หลังเข้ารับการอบรม ท่านมีความรู้ความเข้าใจหลังการฝึกอบรม"
#     part_1 = [["เพศ", "ชาย", "หญิง"], ["ระดับชั้น", "ม.4", "ม.5", "ม.6", "อื่นๆ______"], ["สถานศึกษา", "โรงเรียน", "อบจ.", "อื่นๆ______"], ["สถานที่อบรม", "โรงเรียน", "อบจ.", "อื่นๆ______"], ["ประเภทการอบรม", "อบรม", "สัมมนา", "อื่นๆ______"]]
#     part_2 = [["ความรู้เกี่ยวกับหัวข้อหลังการบรรยาย","การบรรยายชัดเจนเข้าใจง่าย","วิธีถ่ายทอดเนื้อหาน่าสนใจ","เอกสาร/สื่อ ประกอบการบรรยาย","การตอบคำถามตรงประเด็น","ความเหมาะสมของวิทยากรโดยรวม"],
#               ["การรับข่าวประชาสัมพันธ์การจัดอมรม","การประสานงานการต้อนรับ","ระยะเวลาการอมรม","ความพร้อมอุปกรณ์/สื่ออิเล็กทรอนิกส์ต่างๆ","ความเหมาะสมของสถานที่"]]
#     print(createinfsheet(dstpath,head_1,detail1,detail2,part_1,part_2))