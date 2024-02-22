import sys

def chk_part_2_qtn(part_2, part_2_pattern):
    part_2 = part_2.split(',')
    part_2_pattern = part_2_pattern.split(',')
    part_2_ = []
    part_2_temp = []
    if len(part_2) == len(part_2_pattern):
        for i in range(len(part_2)):
            if i == 0 and part_2_pattern[i] == '0':
                part_2_temp.append("Nohead")
            if i != 0 and part_2_pattern[i] == '1':
                part_2_.append(part_2_temp)
                part_2_temp = []
            part_2_temp.append(part_2[i])
        if part_2_temp != []:
            part_2_.append(part_2_temp)
        return part_2_
    else : 
        return [False, "จำนวนคำถามไม่ตรงกับจำนวนรูปแบบหัวข้อ"]

def chk_validate_qtn(part_1, part_2):
    try:
        part_1_check = None
        part_1_ = ""
        for c, i in enumerate(part_1):
            if c != 0: part_1_ += ","
            for cc, ii in enumerate(i[1:]):
                if cc == 0: part_1_ += str(ii)
                else: part_1_ += ":"+str(ii)
            if i[1] != 'n':
                if len(i) != 2:
                    part_1_check = False
        if part_1_check != None :
            part_1_check = "มีคำตอบมากกว่า 1 คำตอบในบางคอลัมน์ที่ส่วนที่ 1"

        part_2_check = None
        part_2_ = ""
        for c, i in enumerate(part_2):
            if c != 0: part_2_ += ","
            for cc, ii in enumerate(i[1:]):
                if cc == 0: part_2_ += str(ii)
                else: part_2_ += ":"+str(ii)
            if i[1] != 'n':
                if len(i) != 2:
                    part_2_check = False
        if part_2_check != None :
            part_2_check = "มีคำตอบมากกว่า 1 คำตอบในบางคอลัมน์ที่ส่วนที่ 2"
        
        check_qtn = True
        if part_1_check != None or part_2_check != None:
            check_qtn = False
        check = [check_qtn, part_1_check, part_2_check]
        return [check, part_1_, part_2_]
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        return "valid Error Line "+str(exc_tb.tb_lineno if exc_tb else None)+" : "+str(e)
        print("valid error :",e)
        return [[False, e, None], None, None]