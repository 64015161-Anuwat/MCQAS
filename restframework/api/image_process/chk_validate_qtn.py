def chk_validate_qtn(part_2, part_2_pattern):
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
        return [False, "จำนวนคถามไม่ตรงกับจำนวนรูปแบบหัวข้อ"]
    