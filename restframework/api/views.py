from math import e
from multiprocessing import process
import os
import csv
from rest_framework import status, viewsets, permissions, routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from tomlkit import key

from .models import *
from .serializers import *

from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string

from .utils.hash_password import *

from .image_process.create_answer_sheet import *
from .image_process.pre_process_ans import *
from .image_process.process_ans import *
from .image_process.chk_validate_ans import *
from .image_process.chk_ans import *

@api_view(['GET'])
def overview(request):
    api_urls = {
        'user': {
            'List': '/user/',
            'Create': '/user/create/',
            'Detail': '/user/detail/<str:pk>/',
            'Update': '/user/update/<str:pk>/',
            'Delete': '/user/delete/<str:pk>/',
            'DuplicateEmail': '/user/duplicate/email/',
            'DuplicateGoogleid': '/user/duplicate/googleid/',
            'Login': '/user/login/',
            'LoginGoogle': '/user/login/google/',
        },
        'checkscore': {
            'List': '/checkscore/',
            'Create': '/checkscore/create/',
            'Detail': '/checkscore/detail/<str:pk>/',
            'Update': '/checkscore/update/<str:pk>/',
            'Delete': '/checkscore/delete/<str:pk>/',
        },
        'exam': {
            'List': '/exam/',
            'Create': '/exam/create/',
            'Detail': '/exam/detail/<str:pk>/',
            'Update': '/exam/update/<str:pk>/',
            'Delete': '/exam/delete/<str:pk>/',
            'UploadCSV': '/exam/upload/csv/',
            'UploadLogo': '/exam/upload/logo/',
        },
        'examanswers': {
            'List': '/examanswers/',
            'Create': '/examanswers/create/',
            'Detail': '/examanswers/detail/<str:pk>/',
            'Update': '/examanswers/update/<str:pk>/',
            'Delete': '/examanswers/delete/<str:pk>/',
            'UploadPaperans': '/examanswers/upload/paperans/',
        },
        'examinformation': {
            'List': '/examinformation/',
            'Create': '/examinformation/create/',
            'Detail': '/examinformation/detail/<str:pk>/',
            'Update': '/examinformation/update/<str:pk>/',
            'Delete': '/examinformation/delete/<str:pk>/',
            'UploadPaperans': '/examinformation/upload/paperans/',
        },
        'errorsanswersheet': {
            'List': '/errorsanswersheet/',
            'Create': '/errorsanswersheet/create/',
            'Detail': '/errorsanswersheet/detail/<str:pk>/',
            'Update': '/errorsanswersheet/update/<str:pk>/',
            'Delete': '/errorsanswersheet/delete/<str:pk>/',
        },
        'lesson': {
            'List': '/lesson/',
            'Create': '/lesson/create/',
            'Detail': '/lesson/detail/<str:pk>/',
            'Update': '/lesson/update/<str:pk>/',
            'Delete': '/lesson/delete/<str:pk>/',
        },
        'lessonanswer': {
            'List': '/lessonanswer/',
            'Create': '/lessonanswer/create/',
            'Detail': '/lessonanswer/detail/<str:pk>/',
            'Update': '/lessonanswer/update/<str:pk>/',
            'Delete': '/lessonanswer/delete/<str:pk>/',
        },
        'queheaddetails': {
            'List': '/queheaddetails/',
            'Create': '/queheaddetails/create/',
            'Detail': '/queheaddetails/detail/<str:pk>/',
            'Update': '/queheaddetails/update/<str:pk>/',
            'Delete': '/queheaddetails/delete/<str:pk>/',
        },
        'quesheet': {
            'List': '/quesheet/',
            'Create': '/quesheet/create/',
            'Detail': '/quesheet/detail/<str:pk>/',
            'Update': '/quesheet/update/<str:pk>/',
            'Delete': '/quesheet/delete/<str:pk>/',
        },
        'quetopicdetails': {
            'List': '/quetopicdetails/',
            'Create': '/quetopicdetails/create/',
            'Detail': '/quetopicdetails/detail/<str:pk>/',
            'Update': '/quetopicdetails/update/<str:pk>/',
            'Delete': '/quetopicdetails/delete/<str:pk>/',
        },
        'queinformation': {
            'List': '/queinformation/',
            'Create': '/queinformation/create/',
            'Detail': '/queinformation/detail/<str:pk>/',
            'Update': '/queinformation/update/<str:pk>/',
            'Delete': '/queinformation/delete/<str:pk>/',
        },
        'request': {
            'List': '/request/',
            'Create': '/request/create/',
            'Detail': '/request/detail/<str:pk>/',
            'Update': '/request/update/<str:pk>/',
            'Delete': '/request/delete/<str:pk>/',
        },
        'role': {
            'List': '/role/',
            'Create': '/role/create/',
            'Detail': '/role/detail/<str:pk>/',
            'Update': '/role/update/<str:pk>/',
            'Delete': '/role/delete/<str:pk>/',
        },
        'sublesson': {
            'List': '/sublesson/',
            'Create': '/sublesson/create/',
            'Detail': '/sublesson/detail/<str:pk>/',
            'Update': '/sublesson/update/<str:pk>/',
            'Delete': '/sublesson/delete/<str:pk>/',
        },
        'subject': {
            'List': '/subject/',
            'Create': '/subject/create/',
            'Detail': '/subject/detail/<str:pk>/',
            'Update': '/subject/update/<str:pk>/',
            'Delete': '/subject/delete/<str:pk>/',
        },
    }
    return Response(api_urls)

##########################################################################################
#- User
@api_view(['GET'])
def userList(request):
    queryset = User.objects.all().order_by('userid')
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def userDetail(request, pk):
    queryset = User.objects.get(userid=pk)
    serializer = UserSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def userCreate(request):
    data = request.data
    salt, hashed_password = hash_password(data['password'])
    data['password'] = hashed_password
    data['salt'] = salt
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"err" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def userUpdate(request, pk):
    user = User.objects.get(userid=pk)
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def userDelete(request, pk):
    user = User.objects.get(userid=pk)
    user.delete()
    return Response({"msg" : "ลบผู้ใช้งานสำเร็จ"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def userDuplicateEmail(request):
    email = request.data['email']
    queryset = User.objects.filter(email=email).count()
    if queryset == 0:
        return Response(True)
    else:
        return Response({"err" : "Email มีผู้ใช้งานแล้ว"}, status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(['POST'])
def userDuplicateGoogleid(request):
    googleid = request.data['googleid']
    queryset = User.objects.filter(googleid=googleid).count()
    if queryset == 0:
        return Response(True)
    else:
        return Response({"err" : "บัญชี Google มีผู้ใช้งานแล้ว"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def userLogin(request):
    email = request.data['email']
    password = request.data['password']
    queryset = User.objects.filter(email=email)
    if queryset.count() > 0:
        salt = queryset[0].salt
        if verify_password(password, salt, queryset[0].password) == True:
            return Response({
                "userid" : queryset[0].userid,
                "email" : queryset[0].email,
                "fullname" : queryset[0].fullname,
                "job" : queryset[0].job,
                "department" : queryset[0].department,
                "faculty" : queryset[0].faculty,
                "workplace" : queryset[0].workplace,
                "tel" : queryset[0].tel,
                            })
        else:
            return Response({"err" : "รหัสผ่านไม่ถูกต้อง"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"err" : "ไม่พบ Email นี้ในระบบ"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def userLoginGoogle(request):
    googleid = request.data['googleid']
    queryset = User.objects.filter(googleid=googleid)
    if queryset.count() > 0:
        return Response({
            "userid" : queryset[0].userid,
            "email" : queryset[0].email,
            "fullname" : queryset[0].fullname,
            "job" : queryset[0].job,
            "department" : queryset[0].department,
            "faculty" : queryset[0].faculty,
            "workplace" : queryset[0].workplace,
            "tel" : queryset[0].tel,
                        })
    else:
        return Response({"err" : "บัญชี Google ไม่ถูกต้อง"})

##########################################################################################
#- Checkscore
@api_view(['GET'])
def checkscoreList(request):
    queryset = Checkscore.objects.all().order_by('scoreid')
    serializer = CheckscoreSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def checkscoreDetail(request, pk):
    queryset = Checkscore.objects.get(scoreid=pk)
    serializer = CheckscoreSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def checkscoreCreate(request):
    serializer = CheckscoreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def checkscoreUpdate(request, pk):
    checkscore = Checkscore.objects.get(scoreid=pk)
    serializer = CheckscoreSerializer(instance=checkscore, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def checkscoreDelete(request, pk):
    checkscore = Checkscore.objects.get(scoreid=pk)
    checkscore.delete()
    return Response({"msg" : "ลบคะแนนสำเร็จ"})

##########################################################################################
#- Exam
@api_view(['GET'])
def examList(request):
    queryset = Exam.objects.all().order_by('examid')
    serializer = ExamSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def examDetail(request, pk):
    queryset = Exam.objects.get(examid=pk)
    serializer = ExamSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def examCreate(request):
    serializer = ExamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def examUpdate(request, pk):
    exam = Exam.objects.get(examid=pk)
    serializer = ExamSerializer(instance=exam, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def examDelete(request, pk):
    exam = Exam.objects.get(examid=pk)
    exam.delete()
    return Response({"msg" : "ลบข้อสอบสำเร็จ"})

@api_view(['POST'])
def examUploadCSV(request):
    file = request.FILES['file']
    if file.name.endswith('.csv'):
        exam = Exam.objects.get(examid=request.data['examid'])
        fs = FileSystemStorage()
        media = "/"+str(request.data['username'])+"/ans/"+str(exam.subid_exam.subid)+"/student_list/"
        media_path = fs.path('')+media
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        for filename in os.listdir(media_path):
            if os.path.isfile(os.path.join(media_path, filename)):
                os.remove(os.path.join(media_path, filename))
        fs.save(media_path+"student_list.csv", file)
        # fs.save(media_path+"student_key.csv", file)

        key_file = open(media_path+"student_key.csv", 'w', encoding='utf-8', newline='')
        writer = csv.writer(key_file)
        list_file = open(media_path+"student_list.csv", 'r', encoding='utf-8', newline='')
        try:
            reader = csv.reader(list_file)
            for index_rows, rows in enumerate(reader):
                if index_rows == 0:
                    row = zip([rows[0]],[rows[1]],[rows[2]],[rows[3]],["key"])
                else:
                    key = get_random_string(length=16)
                    row = zip([rows[0]],[rows[1]],[rows[2]],[rows[3]],[key])
                writer.writerows(row)
        finally:
            key_file.close()
            list_file.close()
        link_csv = request.build_absolute_uri("media/"+media+"student_list.csv")
        val = {"std_csv_path": link_csv}
        serializer = ExamSerializer(instance=exam, data=val)
        if serializer.is_valid():
            serializer.save()

        return Response({"msg" : "อัปโหลดไฟล์รายชื่อสำเร็จ", "std_csv_path" : link_csv})
        
    else:
        return Response({"err" : "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .csv"})

@api_view(['POST'])
def examUploadLogo(request):
    file = request.FILES['file']
    if file.name.endswith('.jpg'):
        exam = Exam.objects.get(examid=request.data['examid'])
        fs = FileSystemStorage()
        media = "/"+str(request.data['username'])+"/ans/"+str(exam.subid_exam.subid)+"/"+str(exam.examid)+"/answersheet_format/"
        media_path = fs.path('')+media
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        for filename in os.listdir(media_path):
            if os.path.isfile(os.path.join(media_path, filename)):
                os.remove(os.path.join(media_path, filename))
        file_content = file.read()
        for i in range(1, 4):
            create_answer_sheet(i, media_path, logo=file_content)
            file.seek(0)
        fs.save(media_path+"Logo.jpg", file)
        val = {"imganswers_format_path": request.build_absolute_uri("/media"+media)}
        serializer = ExamSerializer(instance=exam, data=val)
        if serializer.is_valid():
            serializer.save()
        return Response({"msg" : "อัปโหลดไฟล์ Logo สำเร็จ"})
        
    else:
        return Response({"err" : "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"})


##########################################################################################
#- Examanswers
@api_view(['GET'])
def examanswersList(request):
    queryset = Examanswers.objects.all().order_by('examanswersid')
    serializer = ExamanswersSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def examanswersDetail(request, pk):
    queryset = Examanswers.objects.get(examanswersid=pk)
    serializer = ExamanswersSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def examanswersCreate(request):
    serializer = ExamanswersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def examanswersUpdate(request, pk):
    examanswers = Examanswers.objects.get(examanswersid=pk)
    serializer = ExamanswersSerializer(instance=examanswers, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def examanswersDelete(request, pk):
    examanswers = Examanswers.objects.get(examanswersid=pk)
    examanswers.delete()
    return Response({"msg" : "ลบเฉลยข้อสอบสำเร็จ"})

@api_view(['POST'])
def examanswersUploadPaperans(request):
    file = request.FILES['file']
    if not file.name.endswith('.jpg'):
        return Response({"err" : "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"})
    else:
        answers_ = ''
        examanswers = Examanswers.objects.get(examanswersid=request.data['examanswersid'])
        fs = FileSystemStorage()
        media = "/"+str(request.data['username'])+"/ans/"+str(examanswers.examid_ans.subid_exam.subid)+"/"+str(examanswers.examid_ans.examid)+"/"+str(examanswers.examanswersid)+"/answersheet_scan/"
        media_path = fs.path('')+media
        original_path = media_path+"original/"
        if not os.path.exists(original_path):
            os.makedirs(original_path)
        for filename in os.listdir(original_path):
            if os.path.isfile(os.path.join(original_path, filename)):
                os.remove(os.path.join(original_path, filename))
        fs.save(original_path+file.name, file)

        preprocess_path = media_path+"preprocess/"
        if not os.path.exists(preprocess_path):
            os.makedirs(preprocess_path)
        for filename in os.listdir(preprocess_path):
            if os.path.isfile(os.path.join(preprocess_path, filename)):
                os.remove(os.path.join(preprocess_path, filename))
        pre = pre_process_ans(original_path, preprocess_path, file.name)
        if pre == True:
            data = process_ans(preprocess_path, "pre_"+file.name, 120)
            err = ''
            for i in range(0, len(data[0])):
                if data[0][i] != None:
                    err += str(data[1][i])+"\n"
            if err == '':
                not_n = True
                for i in range(0, len(data[6])):
                    if i != 0 and not_n: answers_ += ','
                    for ii in range(1, len(data[6][i])):
                        if ii == 1 and data[6][i][ii] != 'n' and data[6][i][ii] != 'N':
                            answers_ += str(data[6][i][ii])
                            not_n = True
                        elif ii != 1 and data[6][i][ii] != 'n' and data[6][i][ii] != 'N':
                            answers_ += ':'+str(data[6][i][ii])
                            not_n = True
                        else: not_n = False
                if answers_ == '': return Response({"err" : "ไม่พบคำตอบข้อสอบ"})
                if answers_[-1] == ',': answers_ = answers_[:-1]
                val = {
                "papeans_path": request.build_absolute_uri("/media"+media+"original/"+file.name),
                "answers": answers_,
                }
                serializer = ExamanswersSerializer(instance=examanswers, data=val)
                if serializer.is_valid():
                    serializer.save()
                return Response({
                    "msg" : "อัปโหลดไฟล์สำเร็จ", 
                    "answers" : answers_
                                })
            else:
                err += "ที่ไฟล์: "+file.name
                return Response({"err" : err})
        else:
            return Response({"err" : pre})

##########################################################################################
#- Examinformation
@api_view(['GET'])
def examinformationList(request):
    queryset = Examinformation.objects.all().order_by('examinfoid')
    serializer = ExaminformationSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def examinformationDetail(request, pk):
    queryset = Examinformation.objects.get(examinfoid=pk)
    serializer = ExaminformationSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def examinformationCreate(request):
    serializer = ExaminformationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def examinformationUpdate(request, pk):
    examinformation = Examinformation.objects.get(examinfoid=pk)
    serializer = ExaminformationSerializer(instance=examinformation, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def examinformationDelete(request, pk):
    examinformation = Examinformation.objects.get(examinfoid=pk)
    examinformation.delete()
    return Response({"msg" : "ลบข้อมูลข้อสอบสำเร็จ"})

@api_view(['POST'])
def examinformationUploadPaperans(request):
    res = {"erroranswersheet": [], "examinformation": []}
    subject = Subject.objects.get(subid=request.data['subid'])
    exam = Exam.objects.get(examid=request.data['examid'])
    for file in request.FILES.getlist('file'):
        error = {
            'errorexamid_info' : request.data['examid'],
            "errorstdid": None,
            "errorsubidstd": None,
            "errorexamseatnumber": None,
            "errorsetexaminfo": None,
            "errorsection": None,
            "errorstype": None,
            "errorimgansstd_path": None,
        }

        if file.name.endswith('.jpg'):
            fs = FileSystemStorage()
            default_path = fs.path('')+"/"+str(request.data['username'])+"/ans/"+str(request.data['subid'])+"/"+str(request.data['examid'])+"/answersheet/"
            ori_path = default_path+"original/"
            pre_path = default_path+"preprocess/"
            pre_path_ = "/"+str(request.data['username'])+"/ans/"+str(request.data['subid'])+"/"+str(request.data['examid'])+"/answersheet/"+"preprocess/"
            if not os.path.exists(ori_path):
                os.makedirs(ori_path)
            fs.save(ori_path+file.name, file)
            pre = pre_process_ans(ori_path, pre_path, file.name)
            if pre == True:
                data = process_ans(pre_path, "pre_"+file.name, 120)
                # chk_validate_ans return [check, std_id, sec, seat_id, sub_id, ex_id, answer]
                valid = chk_validate_ans(data[1], data[2], data[3], data[4], data[5], data[6])
                error_valid = ''
                for i in range(0, len(valid[0])):
                    if valid[0][i] != None:
                        error_valid += valid[0][i] + "\n"
                if error_valid == '':

                    queryset = Examanswers.objects.filter(examid_ans=request.data['examid'], setexamans=valid[5])
                    examanswers_serializer = ExamanswersSerializer(queryset, many=False)
                    if examanswers_serializer.data["setexamans"] != None:
                        # chk_ans return [error, ans, chans, max_score, score, right, wrong, rightperchoice, notans, analys]
                        ans = chk_ans(valid[6], exam.numexam, examanswers_serializer.data['answers'], examanswers_serializer.data['scoringcriteria'])
                        examinfo = {
                            "examid_info" : request.data['examid'],
                            "stdid" : valid[1],
                            "subidstd" : valid[4],
                            "examseatnumber" : valid[3],
                            "setexaminfo" : valid[5],
                            "section" : valid[2],
                            "score" : ans[4],
                            "correct" : ans[5],
                            "wrong" : ans[6],
                            "unresponsive" : ans[8],
                            "anschoicestd" : valid[6],
                            "activatekey_exan" : None,
                            "imgansstd_path" : request.build_absolute_uri("/media"+pre_path_+"pre_"+file.name),
                        }
                        examinfo_serializer = ExaminformationSerializer(data=examinfo)
                        if examinfo_serializer.is_valid():
                            examinfo_serializer.save()
                        res["examinformation"].append(examinfo_serializer.data)
                    else :
                        error['errorstdid'] = valid[1]
                        error['errorsection'] = valid[2]
                        error['errorexamseatnumber'] = valid[3]
                        error['errorsubidstd'] = valid[4]
                        error['errorsetexaminfo'] = valid[5]
                        err = "ไม่พบข้อมูลเฉลยข้อสอบ"
                        error['errorstype'] = err
                        serializer = ErrorsanswersheetSerializer(data=error)
                        if serializer.is_valid():
                            serializer.save()
                        res["erroranswersheet"].append(serializer.data)
                else:
                    error['errorstdid'] = valid[1]
                    error['errorsection'] = valid[2]
                    error['errorexamseatnumber'] = valid[3]
                    error['errorsubidstd'] = valid[4]
                    error['errorsetexaminfo'] = valid[5]
                    error['errorstype'] = error_valid
                    serializer = ErrorsanswersheetSerializer(data=error)
                    if serializer.is_valid():
                        serializer.save()
                    res["erroranswersheet"].append(serializer.data)
            else:
                error['errorstype'] = pre
                serializer = ErrorsanswersheetSerializer(data=error)
                if serializer.is_valid():
                    serializer.save()
                res["erroranswersheet"].append(serializer.data)
        else:
            err = "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"
            error['errorstype'] = err
            serializer = ErrorsanswersheetSerializer(data=error)
            if serializer.is_valid():
                serializer.save()
            res["erroranswersheet"].append(serializer.data)
        

    
    return Response(res, status=status.HTTP_201_CREATED)

##########################################################################################
#- ErrorsAnswerSheet
@api_view(['GET'])
def errorsanswersheetList(request):
    queryset = Errorsanswersheet.objects.all().order_by('errorsanssheetid')
    serializer = ErrorsanswersheetSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def errorsanswersheetDetail(request, pk):
    queryset = Errorsanswersheet.objects.get(errorsansid=pk)
    serializer = ErrorsanswersheetSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def errorsanswersheetCreate(request):
    serializer = ErrorsanswersheetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def errorsanswersheetUpdate(request, pk):
    errorsanswersheet = Errorsanswersheet.objects.get(errorsansid=pk)
    serializer = ErrorsanswersheetSerializer(instance=errorsanswersheet, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def errorsanswersheetDelete(request, pk):
    errorsanswersheet = Errorsanswersheet.objects.get(errorsansid=pk)
    errorsanswersheet.delete()
    return Response({"msg" : "ลบข้อมูลข้อสอบสำเร็จ"})

##########################################################################################
#- Lesson
@api_view(['GET'])
def lessonList(request):
    queryset = Lesson.objects.all().order_by('lessonid')
    serializer = LessonSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lessonDetail(request, pk):
    queryset = Lesson.objects.get(lessonid=pk)
    serializer = LessonSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def lessonCreate(request):
    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def lessonUpdate(request, pk):
    lesson = Lesson.objects.get(lessonid=pk)
    serializer = LessonSerializer(instance=lesson, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def lessonDelete(request, pk):
    lesson = Lesson.objects.get(lessonid=pk)
    lesson.delete()
    return Response({"msg" : "ลบบทเรียนสำเร็จ"})

##########################################################################################
#- Lessonanswer
@api_view(['GET'])
def lessonanswerList(request):
    queryset = Lessonanswer.objects.all().order_by('lessonandanswer')
    serializer = LessonanswerSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lessonanswerDetail(request, pk):
    queryset = Lessonanswer.objects.get(lessonandanswer=pk)
    serializer = LessonanswerSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def lessonanswerCreate(request):
    serializer = LessonanswerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def lessonanswerUpdate(request, pk):
    lessonanswer = Lessonanswer.objects.get(lessonandanswer=pk)
    serializer = LessonanswerSerializer(instance=lessonanswer, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def lessonanswerDelete(request, pk):
    lessonanswer = Lessonanswer.objects.get(lessonandanswer=pk)
    lessonanswer.delete()
    return Response({"msg" : "ลบบทเรียนสำเร็จ"})

##########################################################################################
#- Queheaddetails
@api_view(['GET'])
def queheaddetailsList(request):
    queryset = Queheaddetails.objects.all().order_by('queheaddetailsid')
    serializer = QueheaddetailsSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def queheaddetailsDetail(request, pk):
    queryset = Queheaddetails.objects.get(queheaddetailsid=pk)
    serializer = QueheaddetailsSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def queheaddetailsCreate(request):
    serializer = QueheaddetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def queheaddetailsUpdate(request, pk):
    queheaddetails = Queheaddetails.objects.get(queheaddetailsid=pk)
    serializer = QueheaddetailsSerializer(instance=queheaddetails, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def queheaddetailsDelete(request, pk):
    queheaddetails = Queheaddetails.objects.get(queheaddetailsid=pk)
    queheaddetails.delete()
    return Response({"msg" : "ลบหัวข้อแบบสอบถามสำเร็จ"})

##########################################################################################
#- Quesheet
@api_view(['GET'])
def quesheetList(request):
    queryset = Quesheet.objects.all().order_by('quesheetid')
    serializer = QuesheetSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def quesheetDetail(request, pk):
    queryset = Quesheet.objects.get(quesheetid=pk)
    serializer = QuesheetSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def quesheetCreate(request):
    serializer = QuesheetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def quesheetUpdate(request, pk):
    quesheet = Quesheet.objects.get(quesheetid=pk)
    serializer = QuesheetSerializer(instance=quesheet, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def quesheetDelete(request, pk):
    quesheet = Quesheet.objects.get(quesheetid=pk)
    quesheet.delete()
    return Response({"msg" : "ลบแบบสอบถามสำเร็จ"})

##########################################################################################
#- Quetopicdetails
@api_view(['GET'])
def quetopicdetailsList(request):
    queryset = Quetopicdetails.objects.all().order_by('quetopicdetailsid')
    serializer = QuetopicdetailsSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def quetopicdetailsDetail(request, pk):
    queryset = Quetopicdetails.objects.get(quetopicdetailsid=pk)
    serializer = QuetopicdetailsSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def quetopicdetailsCreate(request):
    serializer = QuetopicdetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def quetopicdetailsUpdate(request, pk):
    quetopicdetails = Quetopicdetails.objects.get(quetopicdetailsid=pk)
    serializer = QuetopicdetailsSerializer(instance=quetopicdetails, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def quetopicdetailsDelete(request, pk):
    quetopicdetails = Quetopicdetails.objects.get(quetopicdetailsid=pk)
    quetopicdetails.delete()
    return Response({"msg" : "ลบหัวข้อแบบสอบถามสำเร็จ"})

##########################################################################################
#- Queinformation
@api_view(['GET'])
def queinformationList(request):
    queryset = Queinformation.objects.all().order_by('queinfoid')
    serializer = QueinformationSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def queinformationDetail(request, pk):
    queryset = Queinformation.objects.get(queinfoid=pk)
    serializer = QueinformationSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def queinformationCreate(request):
    serializer = QueinformationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def queinformationUpdate(request, pk):
    queinformation = Queinformation.objects.get(queinfoid=pk)
    serializer = QueinformationSerializer(instance=queinformation, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def queinformationDelete(request, pk):
    queinformation = Queinformation.objects.get(queinfoid=pk)
    queinformation.delete()
    return Response({"msg" : "ลบข้อมูลแบบสอบถามสำเร็จ"})

##########################################################################################
#- Request
@api_view(['GET'])
def requestList(request):
    queryset = Request.objects.all().order_by('requestid')
    serializer = RequestSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def requestDetail(request, pk):
    queryset = Request.objects.get(requestid=pk)
    serializer = RequestSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def requestCreate(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def requestUpdate(request, pk):
    request_ = Request.objects.get(requestid=pk)
    serializer = RequestSerializer(instance=request_, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def requestDelete(request, pk):
    request = Request.objects.get(requestid=pk)
    request.delete()
    return Response({"msg" : "ลบคำร้องขอสำเร็จ"})

##########################################################################################
#- Role
@api_view(['GET'])
def roleList(request):
    queryset = Role.objects.all().order_by('typesid')
    serializer = RoleSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def roleDetail(request, pk):
    queryset = Role.objects.get(typesid=pk)
    serializer = RoleSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def roleCreate(request):
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def roleUpdate(request, pk):
    role = Role.objects.get(typesid=pk)
    serializer = RoleSerializer(instance=role, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def roleDelete(request, pk):
    role = Role.objects.get(typesid=pk)
    role.delete()
    return Response({"msg" : "ลบประเภทผู้ใช้งานสำเร็จ"})

##########################################################################################
#- Sublesson
@api_view(['GET'])
def sublessonList(request):
    queryset = Sublesson.objects.all().order_by('sublessonid')
    serializer = SublessonSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def sublessonDetail(request, pk):
    queryset = Sublesson.objects.get(sublessonid=pk)
    serializer = SublessonSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def sublessonCreate(request):
    serializer = SublessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def sublessonUpdate(request, pk):
    sublesson = Sublesson.objects.get(sublessonid=pk)
    serializer = SublessonSerializer(instance=sublesson, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def sublessonDelete(request, pk):
    sublesson = Sublesson.objects.get(sublessonid=pk)
    sublesson.delete()
    return Response({"msg" : "ลบบทย่อยสำเร็จ"})

##########################################################################################
#- Subject
@api_view(['GET'])
def subjectList(request):
    queryset = Subject.objects.all().order_by('subjectid')
    serializer = SubjectSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def subjectDetail(request, pk):
    queryset = Subject.objects.get(subjectid=pk)
    serializer = SubjectSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def subjectCreate(request):
    serializer = SubjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def subjectUpdate(request, pk):
    subject = Subject.objects.get(subjectid=pk)
    serializer = SubjectSerializer(instance=subject, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def subjectDelete(request, pk):
    subject = Subject.objects.get(subjectid=pk)
    subject.delete()
    return Response({"msg" : "ลบวิชาสำเร็จ"})

##########################################################################################
