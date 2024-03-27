from numpy import std

def chk_validate_ans(stdid, sec_, seatid, subid, exid, ans):
    try:	
        std_check = None
        std_id = ""

        for i in stdid:	
            if i[1] != 'n':
                std_id += str(i[1])
                if len(i) != 2:
                    std_check = False	

        if std_check != None :
            std_id = None
            std_check = "มีคำตอบมากกว่า 1 คำตอบในบางคอลัมน์ที่รหัสนักเรียนนักศึกษา"
        # elif std_id == '':
        #     std_check = "ไม่พบรหัสนักเรียนนักศึกษา"

        sec_check = None
        sec = ""

        for i in sec_:
            if i[1] != 'n':
                sec += str(i[1])
                if len(i) != 2:
                    sec_check = False
        if sec != '':
            sec = str(int(sec))

        if sec_check != None :
            sec = None
            sec_check = "มีคำตอบมากกว่า 1 คำตอบในบางคอลัมน์ที่รหัสกลุ่มเรียน"
        # elif sec == '':
        #     sec_check = "ไม่พบรหัสกลุ่มเรียน"

        seat_check = None
        seat_id = ""

        for i in seatid:
            if i[1] != 'n':
                seat_id += str(i[1])
                if len(i) != 2:
                    seat_check = False

        if seat_check != None :
            seat_id = None
            seat_check = "มีคำตอบมากกว่า 1 คำตอบในบางคอลัมน์ที่รหัสที่นั่งสอบ"
        # elif seat_id == '':
        #     seat_check = "ไม่พบรหัสที่นั่งสอบ"

        sub_check = None
        sub_id = ""

        for i in subid:
            if i[1] != 'n':
                sub_id += str(i[1])
                if len(i) != 2:
                    sub_check = False

        if sub_check != None :
            sub_id = None
            sub_check = "มีคำตอบมากกว่า 1 คำตอบในบางคอลัมน์ที่รหัสวิชา"
        # elif sub_id == '':
        #     sub_check = "ไม่พบรหัสวิชา"

        ex_check = None
        ex_id = ""

        for i in exid:
            if i[1] != 'n':
                ex_id += str(i[1])
                if len(i) !=2:
                    ex_check = False
        if ex_id != '':
            ex_id = str(int(ex_id))

        if ex_check != None :
            ex_id = None
            ex_check = "มีคำตอบมากกว่า 1 คำตอบในบางคอลัมน์ที่ชุดข้อสอบ"
        # elif ex_id == '':
        #     ex_check = "ไม่พบรหัสข้อสอบ"

        ans_check = None
        answer = ""

        for c, ans_ in enumerate(ans):
            if c != 0: answer += ","
            for cc, i in enumerate(ans_[1:]):
                if cc == 0: answer += str(i)
                else: answer += ":"+str(i)

        check = [std_check, sec_check, seat_check, sub_check, ex_check, ans_check]

        return [check, std_id, sec, seat_id, sub_id, ex_id, answer]
    except Exception as e:
  	    return ([e], 0, 0, 0, 0, 0, 0)