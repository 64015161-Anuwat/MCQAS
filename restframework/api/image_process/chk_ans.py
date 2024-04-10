import sys

def chk_ans(ans, chno, chans, measure):
    try:
        ans = ans.split(",")
        ans = [ans[i].split(":") for i in range(len(ans))]

        chans = chans.split(",")
        chans = [chans[i].split(":") for i in range(len(chans))]

        measure = measure.split(",")
        measure = [measure[i].split(":") for i in range(len(measure))]

        max_score = 0
        score = round(0, 2)
        right = 0
        wrong = 0
        notans = 0
        notans_ = False
        rightperchoice = 0
        chk_correct_all = 0
        analys = ""
        countchk = 0

        for ms in measure:
            chno_length = ms[0].split("-")
            if len(chno_length) == 2:
                for i in range(int(chno_length[0])-1, int(chno_length[1])):
                    countchk += 1
                    for ii in range(len(ans[i])):
                        for iii in range(len(chans[i])):
                            if str(ans[i][ii]) == str(chans[i][iii]):
                                chk_correct_all += 1
                                rightperchoice += 1
                        if str(ans[i][ii]) == 'n': 
                            notans += 1
                            notans_ = True

                    max_score += int(ms[2])

                    if ms[1] == '1':
                        if chk_correct_all == len(chans[i]):
                            score += int(ms[2])
                        else:
                            score -= int(ms[3])
                    elif ms[1] == '2':
                        if chk_correct_all <= len(chans[i]):
                            score += int(ms[2])/len(chans[i])*chk_correct_all
                    elif ms[1] == '3':
                        if notans_ == False:
                            if chk_correct_all == len(chans[i]):
                                score += int(ms[2])/len(chans[i])*chk_correct_all
                            elif chk_correct_all == 0:
                                score -= int(ms[2])
                            elif chk_correct_all < len(chans[i]):
                                score -= int(ms[2])-(int(ms[2])/len(chans[i])*chk_correct_all)

                    score = round(score, 2)

                    if i != 0: analys += ","
                    if chk_correct_all == len(chans[i]):
                        right += 1
                        analys += "1"
                    else:
                        wrong += 1
                        analys += "0"
                    chk_correct_all = 0
                    notans_ = False
            else:
                i = int(ms[0])-1
                countchk += 1
                for ii in range(len(ans[i])):
                    for iii in range(len(chans[i])):
                        if str(ans[i][ii]) == str(chans[i][iii]):
                            chk_correct_all += 1
                            rightperchoice += 1
                    if str(ans[i][ii]) == 'n': 
                        notans += 1
                        notans_ = True

                max_score += int(ms[2])
                if ms[1] == '1':
                    if chk_correct_all == len(chans[i]):
                        score += int(ms[2])
                    else:
                        score -= int(ms[3])
                elif ms[1] == '2':
                    if chk_correct_all <= len(chans[i]):
                        score += int(ms[2])/len(chans[i])*chk_correct_all
                elif ms[1] == '3':
                    if notans_ == False:
                        if chk_correct_all == len(chans[i]):
                            score += int(ms[2])/len(chans[i])*chk_correct_all
                        elif chk_correct_all == 0:
                            score -= int(ms[2])
                        elif chk_correct_all < len(chans[i]):
                            score -= int(ms[2])-(int(ms[2])/len(chans[i])*chk_correct_all)
                            
                score = round(score, 2)
                # print('No.', max_score, chans[i], ans[i], int(ms[2])/len(chans[i])*chk_correct_all, score, ms)
                if i != 0: analys += ","
                if chk_correct_all == len(chans[i]):
                    right += 1
                    analys += "1"
                elif chk_correct_all != len(chans[i]) and notans_ == False:
                    wrong += 1
                    analys += "0"
                else:
                    analys += "0"
                chk_correct_all = 0
                notans_ = False
        
        err = ""
        if countchk != chno:
            err = "เกณฑ์คะแนนไม่เท่ากับจำนวนข้อ"
            return (err, None, None, None, None, None, None, None, None, None)
        # print(round(score, 2))
        return (err, ans, chans, max_score, round(score, 2), right, wrong, rightperchoice, notans, analys)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        err = "Error Line "+str(exc_tb.tb_lineno if exc_tb else None)+" : "+str(e)
        return (err, None, None, None, None, None, None, None, None, None)
    
# if __name__ == "__main__":
#     ans = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z"
#     chno = 44
#     chans = "A:B:C:D:G:H,B:D:G,A:B:C:D,B:C:D:E:G:H,B:C:D,B:C:D:E:G,A:B:C:D:G:H,A:B:C:D:E:G:H,A:B:C:D:H,B:C:D:G:H,B:D,A:B,B,B:C:D:G,B:D,B:C:D,B,A:B:D,A:B:D,B:D:G,B:C:D:G,B:G,B:D:F:G,A:B:D,B:C:D:G,B:D:F:G,B:D:G,A:B:D:G,B:G,B:D:G,B:C:D:G,B:C:D:G,B:C:D:E:G,B:C:D:E:G:H,A:B:C:D:G:H,A:B:C:D:G:H,A:B:C:D:E:G:H,B:C:D:G:H,B:C:D:G:H,B:C:D:E:G:H,B:D:F:G,B:D:G,A:B:D:G,B:D:G:H,B:F,C,B:D:F,D:G:H,B:D:G,B:C:D:E:G:H,B:C:D:G:H,B:C:D:F:G,A:B:C:D:G,B:D:F:G,B:C:D:G,B:D:E:G,B:C:D:H,B:D:F,B:C:D,B:D:E:G,B:C:D:E:G,B:D:E:G:H,A:B:C:D:G:H,A:B:C:D:G:H,B:C:D:F:G:H,B:C:D:E:G,A:B:C:D:E:G,B:C:D:E:G:H,B:C:D:E:G,B:C:D:E:G:H,B:D:F:G:H,A:B:C:D:G,B:C:D:G,B:D:E:G,B,B:E,B:C:D,B:C:D:F:G:H,B:C:D:G:H,A:B:D:G,B:C:D:E:G,B:C:D:G:H,B:D:F:G:H,B:C:D:F:G:H,B:D:H,B:C:D,B:C:D:G:H,A:B:C:D:G,B:D:E:G,B:D:G:H,B:C:D:E:G:H,A:B:C:D:G:H,B:D:E:G:H,B:D:H,B:D:E:H,B:C:D:E:H,B:C:D:E:G:H,A:B:C:D:E:F:G:H,A:B:D:F:G:H,B:C:D:E,B:D:E,B:C,A:B,B:C:E,B:C:D,B:F,B:D,B:D:E,B:D:E,B:C:D:G,B:D:F:G,B:C:D:G,A:B:C:D:G,B:D:F:G,B:D:F:G:H,B:D:G:H,B:C:D:G:H,B:C:D:G,B:C:D,B:D:F:G:H"
#     measure = "1-44,1,0,0"
#     a = chk_ans(ans, chno, chans, measure)
#     print(a)
#     # print("Error : "+str(a[0]))
#     # print("ans : "+str(a[1]))
#     # print("chans : "+str(a[2]))
#     # print("maxscore : "+str(a[3]))
#     # print("score : "+str(a[4]))
#     # print("analys : "+str(a[5]))
#     # print("------------------------------------------------")
#     # measure = "1-5,1,0,0,1:6-10,2,0,0,1"
#     # c = chk_ans(b[6], 10, z, measure)
#     # print("Error : "+str(c[0]))
#     # print("ans : "+str(c[1]))
#     # print("chans : "+str(c[2]))