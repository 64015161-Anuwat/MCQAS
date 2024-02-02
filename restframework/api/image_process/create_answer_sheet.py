import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

def create_answer_sheet(c_h, dstpath, logo=None):
    try:
        src =os.getcwd()+"\\api\\image_process\\assets\\"
        height = 2481
        width = 3507
        margin = 50
        bg = (255,255,255)
        black = (0,0,0)
        cirtext = (70,70,70)

        bgimg = np.zeros((height,width,3), np.uint8)
        bgimg[:,:] = bg

        cv2.rectangle(bgimg,(margin,margin),(width-margin,height-margin),black,3)

        qrcode = cv2.imread(src+"qrcode.jpg")
        qrcode = cv2.resize(qrcode,(80,80))

        x_offset=width-margin-80
        y_offset=height-margin-80
        bgimg [y_offset:y_offset+qrcode.shape[0], x_offset:x_offset+qrcode.shape[1]]=qrcode

        if logo is None:
            detail = cv2.imread(src+"detail.jpg")
            x_offset=margin+3
            y_offset=margin+3
            bgimg [y_offset:y_offset+detail.shape[0], x_offset:x_offset+detail.shape[1]]=detail

            logo_kmitl = cv2.imread(src+"logo.jpg")
            x_offset=margin+100
            y_offset=margin+20
            bgimg [y_offset:y_offset+logo_kmitl.shape[0], x_offset:x_offset+logo_kmitl.shape[1]]=logo_kmitl
        else:
            detail = cv2.imread(src+"detail2.jpg")
            x_offset=margin+3
            y_offset=margin+3
            bgimg [y_offset:y_offset+detail.shape[0], x_offset:x_offset+detail.shape[1]]=detail

            logo_ = np.frombuffer(logo, np.uint8)
            logo_ = cv2.imdecode(logo_, cv2.IMREAD_UNCHANGED)
            logo_ = cv2.resize(logo_,(300,300))
            x_offset=margin+35
            y_offset=margin+3
            bgimg [y_offset:y_offset+logo_.shape[0], x_offset:x_offset+logo_.shape[1]]=logo_


        posstartnum = (219,1325)
        sizefont = 1
        font1 = cv2.FONT_HERSHEY_COMPLEX
        font2 = cv2.FONT_HERSHEY_SIMPLEX
        indnum = 525
        indchoice = 50
        spacechoice = 72
        imgno = bgimg
        for startnum in range(120):
            pos = (int(posstartnum[1]+(indnum*(startnum//30))),int(posstartnum[0]+spacechoice*(startnum%30)))
            imgno = cv2.putText(bgimg,str(startnum+1), pos, font1, sizefont, black,2)


        posstartchoice = (posstartnum[1]+100,posstartnum[0]-10)
        imgchoice = imgno
        for nochoice in range(120):
            for startchoice in range(8):
                pos = (int(posstartchoice[0]+(indchoice*startchoice)+(indnum*(nochoice//30))),int(posstartchoice[1]+spacechoice*(nochoice%30)))
                imgchoice=cv2.circle(imgno, pos, 16, cirtext, 1)


        chafont = 0.9
        poscharchoice = (posstartnum[1]+90,posstartnum[0])

        ch = c_h

        if ch==1:
            c_h = ['A','B','C','D','E','F','G','H']
        elif ch==2:
            c_h = ['1','2','3','4','5','6','7','8']
        elif ch ==3:
            c_h = ['ก','ข','ค','ง','จ','ฉ','ช','ซ']

        draw = None
        pil_img = None
        fonttext2 = None
        if ch == 3 :
            img = cv2.cvtColor(imgchoice, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img)
            draw = ImageDraw.Draw(pil_img)
            fonttext2 = ImageFont.truetype(src+'_arisa.ttf',40)
        
        imgchchoice = imgchoice
        for nochoice in range(120):
            for charchoice in range(len(c_h)):
                if ch == 3 and draw is not None:
                    draw.text(((poscharchoice[0]+3)+(indchoice*charchoice)+(indnum *(nochoice//30)),(poscharchoice[1]-35)+spacechoice*(nochoice%30)), c_h[charchoice],cirtext, font=fonttext2)
                else:
                    pos = (int(poscharchoice[0]+(indchoice*charchoice)+(indnum *(nochoice//30))),int(poscharchoice[1]+spacechoice*(nochoice%30)))
                    imgchchoice = cv2.putText(imgchoice,c_h[charchoice], pos, font2, chafont , cirtext,1)
        if ch == 3 :
            imgchchoice = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        mainmarkhor = (20,40)
        posmainmarkhor = (1325,50)
        imgmark = imgchchoice
        for mark1 in range(8):
            newpos1 = (int(posmainmarkhor[0]+indnum*(mark1%4)), int(posmainmarkhor[1]+2341*(mark1//4)))
            # pos = (int(newpos1[0]+(mainmarkhor[0]/2)),int(newpos1[1]+(mainmarkhor[1]/2)))
            pos = (int(newpos1[0]+mainmarkhor[0]), int(newpos1[1]+mainmarkhor[1]))
            imgmark = cv2.rectangle(imgchchoice,newpos1, pos,black,-1)

        mainmarkver = (40,20)
        posmainmarkver = (1245,127)
        imgmark1 = imgmark
        for mark2 in range(8):
            newpos2 = (int(posmainmarkver[0]+2172*(mark2//4)),int(posmainmarkver[1]+720*(mark2%4)))
            pos = (int(newpos2[0]+mainmarkver[0]), int(newpos2[1]+mainmarkver[1]))
            imgmark1 = cv2.rectangle(imgmark,newpos2, pos,black,-1)

        submark = (20,20)
        possubmark = (1416,margin+2358)
        imgmark2 = imgmark1
        for mark3 in range(4):
            for mark4 in range(8):
                newpos3 = (possubmark[0]+(50*mark4)+(mark3*indnum) ,possubmark[1])
                imgmark2 = cv2.rectangle(imgmark1,newpos3,(newpos3[0]+submark[0],newpos3[1]+submark[1]),black,-1)

        begin1 = (100,795)
        begin2 = (100,1600)
        infsize = (1110,785)
        graprow = 60
        grapcol = 74

        #mainrect1
        cv2.rectangle(imgmark2,begin1,(begin1[0]+infsize[0], begin1[1]+infsize[1]),black,3)
        #subline1
        cv2.rectangle(imgmark2,(begin1[0],begin1[1]+50), (begin1[0]+infsize[0],begin1[1]+infsize[1]),black,2)
        #subline2
        cv2.rectangle(imgmark2,(begin1[0],begin1[1]+75), (begin1[0]+infsize[0],begin1[1]+infsize[1]),black,2)

        init1 = (128,864)
        init2 = (202,1669)

        for index1 in range(15):
            cv2.putText(imgmark2,str(((index1)%13)+1),(init1[0]+(grapcol*index1),init1[1]), font1, 0.6 , black,1)

        #subline3
        cv2.rectangle(imgmark2,(begin1[0],begin1[1]+125), (begin1[0]+infsize[0],begin1[1]+infsize[1]),black,2)


        cv2.line(imgmark2, (begin1[0]+grapcol*13,begin1[1]), (begin1[0]+grapcol*13,begin1[1]+infsize[1]), black, 2,)
        cv2.line(imgmark2, (begin1[0]+grapcol*14,begin1[1]+50),(begin1[0]+grapcol*14, begin1[1]+infsize[1]), black, 2,)



        for lineloop1 in range(13):
            cv2.line(imgmark2, (begin1[0]+(grapcol*lineloop1),begin1[1]+50),(begin1[0]+(grapcol*lineloop1), begin1[1]+infsize[1]), black, 2,)


        number1 = (136,980)
        number2 = (137,1785)
        synnum1 = (128,989)
        synnum2 = (128,1794)


        for mark6 in range(15):
            for mark5 in range(10):
                cv2.circle(imgmark2, (number1[0]+(mark6*grapcol),number1[1]+(graprow*mark5)), 16, cirtext,1)


        for runnum1 in range(15):
            for numchoice1 in range(10):
                cv2.putText(imgmark2,str(numchoice1),(synnum1[0]+(runnum1*grapcol),synnum1[1]+(graprow*numchoice1)), font2, chafont , cirtext,1)

        #mainrect2
        cv2.rectangle(imgmark2,begin2,(begin2[0]+infsize[0],begin2[1]+infsize[1]),black,3)
        #subline1
        cv2.line(imgmark2, (begin2[0]+grapcol,begin2[1]+50), (begin2[0]+grapcol*15, begin2[1]+50), black, 2,)

        #subline2
        cv2.rectangle(imgmark2,(begin2[0],begin2[1]+75), (begin2[0]+infsize[0],begin2[1]+infsize[1]),black,2)
        a=0
        b=0
        for index2 in range(14):
            if index2 >11:
                b=b+1
                cv2.putText(imgmark2,str(b),(init2[0]+(grapcol*index2),init2[1]), font1, 0.6 , black,1)
            elif  index2 >3:
                a=a+1
                cv2.putText(imgmark2,str(a),(init2[0]+(grapcol*index2),init2[1]), font1, 0.6 , black,1)
            else:
                cv2.putText(imgmark2,str(index2+1),(init2[0]+(grapcol*index2),init2[1]), font1, 0.6 , black,1)

        #subline3
        cv2.rectangle(imgmark2,(begin2[0],begin2[1]+125), (begin2[0]+infsize[0],begin2[1]+infsize[1]),black,2)

        #1
        cv2.line(imgmark2, (begin2[0]+grapcol,begin2[1]), (begin2[0]+grapcol,begin2[1]+infsize[1]), black, 2,)

        for lineloop2 in range(15):
            cv2.line(imgmark2, (begin2[0]+(grapcol*lineloop2),begin2[1]+50),(begin2[0]+(grapcol*lineloop2), begin2[1]+infsize[1]), black, 2,)

        #2
        cv2.line(imgmark2, (begin2[0]+grapcol*5,begin2[1]), (begin2[0]+grapcol*5,begin2[1]+infsize[1]), black, 2,)
        #3
        cv2.line(imgmark2, (begin2[0]+grapcol*13,begin2[1]), (begin2[0]+grapcol*13,begin2[1]+infsize[1]), black, 2,)

        for mark6 in range(15):
            for mark5 in range(10):
                cv2.circle(imgmark2, (number2[0]+(mark6*grapcol),number2[1]+(graprow*mark5)), 16, cirtext,1)

        rw = ['A','B','C','D','E','F','G','H','I','J']

        for runnum2 in range(15):
            for numchoice2 in range(10):
                if runnum2 == 0:
                    cv2.putText(imgmark2,rw[numchoice2],(synnum2[0]+(runnum2*grapcol),synnum2[1]+(graprow*numchoice2)), font2, chafont , cirtext,1)
                else:
                    cv2.putText(imgmark2,str(numchoice2),(synnum2[0]+(runnum2*grapcol),synnum2[1]+(graprow*numchoice2)), font2, chafont , cirtext,1)


        if ch==1:
            cv2.imwrite(dstpath+"answersheet_eng.jpg", imgmark2)
        elif ch==2:
            cv2.imwrite(dstpath+"answersheet_num.jpg", imgmark2)
        elif ch ==3:
            cv2.imwrite(dstpath+"answersheet_thai.jpg", imgmark2)

        return True
    except Exception as e:
        print(e)
        return False
   
if __name__ == '__main__':
    create_answer_sheet(1, "")
    create_answer_sheet(2, "")
    create_answer_sheet(3, "")