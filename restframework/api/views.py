from math import e
import os
import sys, errno  
import shutil
import csv
import json
import datetime
import pandas as pd
from h11 import Data
from pandas import read_csv
from rest_framework import status, viewsets, permissions, routers
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
from .image_process.process_qrcode import *
from .image_process.create_questionnaire_sheet import *
from .image_process.pre_process_qtn import *
from .image_process.process_qtn import *
from .image_process.chk_validate_qtn import *

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
            'UploadPaper': '/examanswers/upload/paper/',
        },
        'examinformation': {
            'List': '/examinformation/',
            'Create': '/examinformation/create/',
            'Detail': '/examinformation/detail/<str:pk>/',
            'Update': '/examinformation/update/<str:pk>/',
            'Delete': '/examinformation/delete/<str:pk>/',
            'UploadPaper': '/examinformation/upload/paper/',
        },
        'chapter': {
            'List': '/chapter/',
            'Create': '/chapter/create/',
            'Detail': '/chapter/detail/<str:pk>/',
            'Update': '/chapter/update/<str:pk>/',
            'Delete': '/chapter/delete/<str:pk>/',
        },
        'chapteranswer': {
            'List': '/chapteranswer/',
            'Create': '/chapteranswer/create/',
            'Detail': '/chapteranswer/detail/<str:pk>/',
            'Update': '/chapteranswer/update/<str:pk>/',
            'Delete': '/chapteranswer/delete/<str:pk>/',
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
            'UploadPaper': '/queinformation/upload/paper/',
        },
        'request': {
            'List': '/request/',
            'Create': '/request/create/',
            'Detail': '/request/detail/<str:pk>/',
            'Update': '/request/update/<str:pk>/',
            'Delete': '/request/delete/<str:pk>/',
        },
        'type': {
            'List': '/type/',
            'Create': '/type/create/',
            'Detail': '/type/detail/<str:pk>/',
            'Update': '/type/update/<str:pk>/',
            'Delete': '/type/delete/<str:pk>/',
        },
        'subchapter': {
            'List': '/subchapter/',
            'Create': '/subchapter/create/',
            'Detail': '/subchapter/detail/<str:pk>/',
            'Update': '/subchapter/update/<str:pk>/',
            'Delete': '/subchapter/delete/<str:pk>/',
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
    data['createtimeuser'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"err" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def userUpdate(request, pk):
    user = User.objects.get(userid=pk)
    data = request.data
    salt, hashed_password = hash_password(data['password'])
    data['password'] = hashed_password
    data['salt'] = salt
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
                "googleid" : queryset[0].googleid,
                "usageformat" : queryset[0].usageformat,
                "e_kyc" : queryset[0].e_kyc,
                "typesid" : queryset[0].typesid.typesid,
            }, status=status.HTTP_200_OK)
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
                "googleid" : queryset[0].googleid,
                "usageformat" : queryset[0].usageformat,
                "e_kyc" : queryset[0].e_kyc,
                "typesid" : queryset[0].typesid.typesid,
        }, status=status.HTTP_200_OK)
    else:
        return Response({"err" : "บัญชี Google ไม่ถูกต้อง"}, status=status.HTTP_401_UNAUTHORIZED)

##########################################################################################
#- Exam
@api_view(['GET'])
def examList(request):
    queryset = Exam.objects.all().order_by('examid')
    serializer = ExamSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def examDetail(request, pk):
    queryset = Exam.objects.get(examid=pk)
    serializer = ExamSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def examCreate(request):
    data = request.data
    data['imganswersheetformat_path'] = request.build_absolute_uri("/media/original_answersheet/")
    data['deletetimeexam'] = None
    data['createtimeexam'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    exam = Exam.objects.filter(subid=data['subid'])
    user = User.objects.get(userid=data['userid'])
    if exam.count() < user.typesid.limitexam:
        serializer = ExamSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"err" : "จำนวนข้อสอบของรายวิชานี้เกินที่กำหนด"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def examUpdate(request, pk):
    exam = Exam.objects.get(examid=pk)
    serializer = ExamSerializer(instance=exam, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def examDelete(request, pk):
    exam = Exam.objects.get(examid=pk)
    exam.delete()
    return Response({"msg" : "ลบข้อสอบสำเร็จ"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def examUploadCSV(request):
    file = request.FILES['file']
    user = User.objects.get(userid=request.data['userid'])
    if file.name.endswith('.csv'):
        exam = Exam.objects.get(examid=request.data['examid'])
        fs = FileSystemStorage()
        print(exam.subid)
        media = "/"+str(user.fullname)+"/ans/"+str(exam.subid.subid)+"/"+str(exam.examid)+"/student_list/"
        media_path = fs.path('')+media
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        for filename in os.listdir(media_path):
            if os.path.isfile(os.path.join(media_path, filename)):
                os.remove(os.path.join(media_path, filename))
        fs.save(media_path+"student_list.csv", file)

        link_csv = request.build_absolute_uri("/media/"+media+"student_list.csv")
        val = {"std_csv_path": link_csv}
        serializer = ExamSerializer(instance=exam, data=val)
        if serializer.is_valid():
            serializer.save()

        return Response({"msg" : "อัปโหลดไฟล์รายชื่อสำเร็จ", "std_csv_path" : link_csv}, status=status.HTTP_201_CREATED)
        
    else:
        return Response({"err" : "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .csv"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def examUploadLogo(request):
    file = request.FILES['file']
    user = User.objects.get(userid=request.data['userid'])
    if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg'):
        exam = Exam.objects.get(examid=request.data['examid'])
        fs = FileSystemStorage()
        media = "/"+str(user.fullname)+"/ans/"+str(exam.subid.subid)+"/"+str(exam.examid)+"/answersheet_format/"
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
        imganswersheetformat_path = request.build_absolute_uri("/media"+media)
        val = {"imganswersheetformat_path": imganswersheetformat_path}
        serializer = ExamSerializer(instance=exam, data=val)
        if serializer.is_valid():
            serializer.save()
        return Response({"msg" : "อัปโหลดไฟล์ Logo สำเร็จ", "imganswersheetformat_path" : imganswersheetformat_path}, status=status.HTTP_201_CREATED)
        
    else:
        return Response({"err" : "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"}, status=status.HTTP_400_BAD_REQUEST)


##########################################################################################
#- Examanswers
@api_view(['GET'])
def examanswersList(request):
    queryset = Examanswers.objects.all().order_by('examanswersid')
    serializer = ExamanswersSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def examanswersDetail(request, pk):
    queryset = Examanswers.objects.get(examanswersid=pk)
    serializer = ExamanswersSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def examanswersCreate(request):
    data = request.data
    exam = Exam.objects.get(examid=data['examid'])
    examanswer = Examanswers.objects.filter(examid=data['examid'])
    if examanswer.count() < int(exam.numberofexamsets):
        serializer = ExamanswersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"err" : "จำนวนชุดข้อสอบครบแล้ว"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def examanswersUpdate(request, pk):
    examanswers = Examanswers.objects.get(examanswersid=pk)
    serializer = ExamanswersSerializer(instance=examanswers, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def examanswersDelete(request, pk):
    examanswers = Examanswers.objects.get(examanswersid=pk)
    examanswers.delete()
    return Response({"msg" : "ลบเฉลยข้อสอบสำเร็จ"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def examanswersUploadPaper(request):
    file = request.FILES['file']
    user = User.objects.get(userid=request.data['userid'])
    print(file.name)
    if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg'):
        answers_ = ''
        fs = FileSystemStorage()
        media = "/"+str(user.fullname)+"/ans/temp/"
        media_path = fs.path('')+media
        original_path = media_path+"original/"
        if not os.path.exists(original_path):
            os.makedirs(original_path)
        fs.save(original_path+file.name, file)

        preprocess_path = media_path+"preprocess/"
        if not os.path.exists(preprocess_path):
            os.makedirs(preprocess_path)
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
                if answers_ == '': return Response({"err" : "ไม่พบคำตอบข้อสอบ"}, status=status.HTTP_400_BAD_REQUEST)
                if answers_[-1] == ',': answers_ = answers_[:-1]
                return Response({
                    "msg" : "อัปโหลดไฟล์สำเร็จ", 
                    "choiceanswers" : answers_
                }, status=status.HTTP_201_CREATED)
            else:
                err += "ที่ไฟล์: "+file.name
                return Response({"err" : err}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"err" : pre}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"err" : "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"}, status=status.HTTP_400_BAD_REQUEST)
        

##########################################################################################
#- Examinformation
@api_view(['GET'])
def examinformationList(request):
    queryset = Examinformation.objects.all().order_by('examinfoid')
    serializer = ExaminformationSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def examinformationDetail(request, pk):
    queryset = Examinformation.objects.get(examinfoid=pk)
    serializer = ExaminformationSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def examinformationCreate(request):
    serializer = ExaminformationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def examinformationUpdate(request, pk):
    user = User.objects.get(userid=request.data['userid'])
    exam = Exam.objects.get(examid=request.data['examid'])
    examinformation = Examinformation.objects.get(examinfoid=pk)
    file = request.FILES['file'] if 'file' in request.FILES else False
    if file == False:
        examinformation_update = json.loads(request.data['examinformation'])
        serializer = ExaminformationSerializer(instance=examinformation, data=examinformation_update)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        fs = FileSystemStorage()
        default_path = "/"+str(user.fullname)+"/ans/"+str(request.data['subid'])+"/"+str(request.data['examid'])+"/answersheet/"
        ori_path = fs.path('')+default_path+"original/"
        pre_path = fs.path('')+default_path+"preprocess/"
        pre_path_ = "/"+str(user.fullname)+"/ans/"+str(request.data['subid'])+"/"+str(request.data['examid'])+"/answersheet/"+"preprocess/"
        os.makedirs(ori_path, exist_ok=True)

        examinfo = {
            "examid" : request.data['examid'],
            "stdemail" : None,
            "stdid" : None,
            "subjectidstd" : None,
            "examseatnumber" : None,
            "setexaminfo" : None,
            "section" : None,
            "score" : None,
            "correct" : None,
            "wrong" : None,
            "unresponsive" : None,
            "itemanalysis": None,
            "anschoicestd" : None,
            "activatekey_exan" : None,
            "imgansstd_path" : None,
            "errorstype" : None
        }
        if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg'):
            old_img = examinformation.imgansstd_path.split("/")[-1]
            print(old_img)
            if os.path.exists(ori_path):
                os.remove(ori_path+old_img)
            if os.path.exists(pre_path):
                os.remove(pre_path+"pre_"+old_img)
            fs.save(ori_path+file.name, file)
            img_link = request.build_absolute_uri("/media"+default_path+"original/"+file.name)
            pre = pre_process_ans(ori_path, pre_path, file.name)
            examinfo['imgansstd_path'] = img_link

            if pre == True:
                data = process_ans(pre_path, "pre_"+file.name, 120)
                # chk_validate_ans return [check, std_id, sec, seat_id, sub_id, ex_id, answer]
                valid = chk_validate_ans(data[1], data[2], data[3], data[4], data[5], data[6])
                error_valid = ''
                error_valid = '\n'.join([error for error in valid[0] if error is not None])
                examinfo['stdid'] = valid[1]
                examinfo['section'] = valid[2]
                examinfo['examseatnumber'] = valid[3]
                examinfo['subjectidstd'] = valid[4]
                if valid[5] == '' : valid[5] = None
                examinfo['setexaminfo'] = valid[5]
                examinfo['anschoicestd'] = valid[6]

                if error_valid == '':
                    csv_path = fs.path('')+"/"+str(user.fullname)+"/ans/"+str(request.data['subid'])+"/"+str(request.data['examid'])+"/student_list/student_list.csv"
                    df = pd.read_csv(csv_path)
                    df['รหัสนักศึกษา'] = df['รหัสนักศึกษา'].astype(str)
                    index = df[df['รหัสนักศึกษา'] == valid[1]].index
                    err_std = "ไม่พบรหัสนักศึกษาในรายชื่อ" if index.empty else ''
                    examinfo['stdemail'] = df['email'][index[0]] if not index.empty else None

                    queryset = Examanswers.objects.get(examid=request.data['examid'], examnoanswers=valid[5])
                    examanswers_serializer = ExamanswersSerializer(queryset, many=False)
                    
                    if examanswers_serializer.data['examanswersid'] != '':
                        # chk_ans return [error, ans, chans, max_score, score, right, wrong, rightperchoice, notans, analys]
                        ans = chk_ans(valid[6], exam.numberofexams, examanswers_serializer.data['choiceanswers'], examanswers_serializer.data['scoringcriteria'])
                        examinfo['score'] = ans[4]
                        examinfo['correct'] = ans[5]
                        examinfo['wrong'] = ans[6]
                        examinfo['unresponsive'] = ans[8]
                        examinfo['itemanalysis'] = ans[9]
                        if ans[0] == '' and err_std == '':
                            examinfo['errorstype'] = None
                        elif ans[0] != '' and err_std == '':
                            examinfo['errorstype'] = ans[0]
                        elif ans[0] == '' and err_std != '':
                            examinfo['errorstype'] = err_std
                        else :
                            examinfo['errorstype'] = err_std+","+ans[0]
                    else :
                        err_set = "ไม่พบข้อมูลเฉลยข้อสอบ"
                        examinfo['errorstype'] = err_set if err_std == '' else err_set+","+err_std
                else:
                    examinfo['errorstype'] = error_valid
            else:
                examinfo['errorstype'] = pre
        else:
            return Response({"err" : "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ExaminformationSerializer(instance=examinformation, data=examinfo)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)    

@api_view(['DELETE'])
def examinformationDelete(request, pk):
    examinformation = Examinformation.objects.get(examinfoid=pk)
    examinformation.delete()
    return Response({"msg" : "ลบข้อมูลข้อสอบสำเร็จ"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def examinformationUploadPaper(request):
    res = []
    user = User.objects.get(userid=request.data['userid'])
    exam = Exam.objects.get(examid=request.data['examid'])
    fs = FileSystemStorage()
    default_path = "/"+str(user.fullname)+"/ans/"+str(request.data['subid'])+"/"+str(request.data['examid'])+"/answersheet/"
    ori_path = fs.path('')+default_path+"original/"
    pre_path = fs.path('')+default_path+"preprocess/"
    pre_path_ = "/"+str(user.fullname)+"/ans/"+str(request.data['subid'])+"/"+str(request.data['examid'])+"/answersheet/"+"preprocess/"
    os.makedirs(ori_path, exist_ok=True)

    for file in request.FILES.getlist('file'):
        examinfo = {
            "examid" : request.data['examid']
        }
        if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg'):
            fs.save(ori_path+file.name, file)
            img_link = request.build_absolute_uri("/media"+default_path+"original/"+file.name)
            pre = pre_process_ans(ori_path, pre_path, file.name)
            examinfo['imgansstd_path'] = img_link

            if pre == True:
                data = process_ans(pre_path, "pre_"+file.name, exam.numberofexams)
                # chk_validate_ans return [check, std_id, sec, seat_id, sub_id, ex_id, answer]
                valid = chk_validate_ans(data[1], data[2], data[3], data[4], data[5], data[6])
                error_valid = ''
                error_valid = '\n'.join([error for error in valid[0] if error is not None])
                examinfo['stdid'] = valid[1]
                examinfo['section'] = valid[2]
                examinfo['examseatnumber'] = valid[3]
                examinfo['subjectidstd'] = valid[4]
                if valid[5] == '' : valid[5] = None
                examinfo['setexaminfo'] = valid[5]
                examinfo['anschoicestd'] = valid[6]

                if error_valid == '':
                    csv_path = fs.path('')+"/"+str(user.fullname)+"/ans/"+str(request.data['subid'])+"/"+str(request.data['examid'])+"/student_list/student_list.csv"
                    df = pd.read_csv(csv_path)
                    df['รหัสนักศึกษา'] = df['รหัสนักศึกษา'].astype(str)
                    index = df[df['รหัสนักศึกษา'] == valid[1]].index
                    err_std = "ไม่พบรหัสนักศึกษาในรายชื่อ" if index.empty else ''
                    examinfo['stdemail'] = df['email'][index[0]] if not index.empty else None

                    queryset = Examanswers.objects.get(examid=request.data['examid'], examnoanswers=valid[5])
                    examanswers_serializer = ExamanswersSerializer(queryset, many=False)
                    
                    if examanswers_serializer.data['examanswersid'] != '':
                        # chk_ans return [error, ans, chans, max_score, score, right, wrong, rightperchoice, notans, analys]
                        ans = chk_ans(valid[6], exam.numberofexams, examanswers_serializer.data['choiceanswers'], examanswers_serializer.data['scoringcriteria'])
                        examinfo['score'] = ans[4]
                        examinfo['correct'] = ans[5]
                        examinfo['wrong'] = ans[6]
                        examinfo['unresponsive'] = ans[8]
                        examinfo['itemanalysis'] = ans[9]
                        if ans[0] == '' and err_std == '':
                            examinfo['errorstype'] = None
                        elif ans[0] != '' and err_std == '':
                            examinfo['errorstype'] = ans[0]
                        elif ans[0] == '' and err_std != '':
                            examinfo['errorstype'] = err_std
                        else :
                            examinfo['errorstype'] = err_std+","+ans[0]
                    else :
                        err_set = "ไม่พบข้อมูลเฉลยข้อสอบ"
                        examinfo['errorstype'] = err_set if err_std == '' else err_set+","+err_std
                else:
                    examinfo['errorstype'] = error_valid
            else:
                examinfo['errorstype'] = pre
        else:
            examinfo['errorstype'] = "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"

        examinfo['createtimeexaminfo'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        examinfo_serializer = ExaminformationSerializer(data=examinfo)

        if examinfo_serializer.is_valid():
            examinfo_serializer.save()
        else:
            return Response({"err" : examinfo_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        res.append(examinfo_serializer.data)
    return Response(res, status=status.HTTP_201_CREATED)

##########################################################################################
#- chapter
@api_view(['GET'])
def chapterList(request):
    queryset = Chapter.objects.all().order_by('chapterid')
    serializer = ChapterSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def chapterDetail(request, pk):
    queryset = Chapter.objects.get(chapterid=pk)
    serializer = ChapterSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def chapterCreate(request):
    serializer = ChapterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def chapterUpdate(request, pk):
    chapter = Chapter.objects.get(chapterid=pk)
    serializer = ChapterSerializer(instance=chapter, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def chapterDelete(request, pk):
    chapter = Chapter.objects.get(chapterid=pk)
    chapter.delete()
    return Response({"msg" : "ลบบทเรียนสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- chapteranswer
@api_view(['GET'])
def chapteranswerList(request):
    queryset = Chapteranswer.objects.all().order_by('chapterandanswerid')
    serializer = ChapteranswerSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def chapteranswerDetail(request, pk):
    queryset = Chapteranswer.objects.get(chapterandanswerid=pk)
    serializer = ChapteranswerSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def chapteranswerCreate(request):
    serializer = ChapteranswerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def chapteranswerUpdate(request, pk):
    chapteranswer = Chapteranswer.objects.get(chapterandanswerid=pk)
    serializer = ChapteranswerSerializer(instance=chapteranswer, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def chapteranswerDelete(request, pk):
    chapteranswer = Chapteranswer.objects.get(chapterandanswerid=pk)
    chapteranswer.delete()
    return Response({"msg" : "ลบบทเรียนสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- Quesheet
@api_view(['GET'])
def quesheetList(request):
    queryset = Quesheet.objects.all().order_by('quesheetid')
    serializer = QuesheetSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def quesheetDetail(request, pk):
    queryset = Quesheet.objects.get(quesheetid=pk)
    serializer = QuesheetSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def quesheetCreate(request):
    user = User.objects.get(userid=request.data['userid'])
    data = request.data
    quesheet_data = json.loads(data['quesheet'])
    queheaddetails_data = json.loads(data['queheaddetails'])
    quetopicdetails_data = json.loads(data['quetopicdetails'])
    head_1 = quesheet_data['quesheettopicname']
    detail_1 = quesheet_data['detailslineone']
    detail_2 = quesheet_data['detailslinetwo']
    part_1 = [queheaddetails_data['quehead1'].split(','), 
              queheaddetails_data['quehead2'].split(','), 
              queheaddetails_data['quehead3'].split(','), 
              queheaddetails_data['quehead4'].split(','), 
              queheaddetails_data['quehead5'].split(',')]
    part_2 = chk_validate_qtn(quetopicdetails_data['quetopicdetails'], quetopicdetails_data['quetopicformat'])
    if part_2[0] != False:
        quesheet_data['createtimequesheet'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        quesheet_serializer = QuesheetSerializer(data=quesheet_data)
        if quesheet_serializer.is_valid():
            quesheet_serializer.save()
        else:
            return Response({"err" : quesheet_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        queheaddetails_data['quesheetid'] = quesheet_serializer.data['quesheetid']
        queheaddetails_serializer = QueheaddetailsSerializer(data=queheaddetails_data)
        if queheaddetails_serializer.is_valid():
            queheaddetails_serializer.save()
        else:
            return Response({"err" : queheaddetails_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        quetopicdetails_data['quesheetid'] = quesheet_serializer.data['quesheetid']
        quetopicdetails_serializer = QuetopicdetailsSerializer(data=quetopicdetails_data)
        if quetopicdetails_serializer.is_valid():
            quetopicdetails_serializer.save()
        else:
            return Response({"err" : quetopicdetails_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        fs = FileSystemStorage()
        media = "/"+str(user.fullname)+"/qtn/"+str(quesheet_serializer.data['quesheetid'])+"/original_sheet/"
        media_path = fs.path('')+media
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        for filename in os.listdir(media_path):
            if os.path.isfile(os.path.join(media_path, filename)):
                os.remove(os.path.join(media_path, filename))
        qrcode_path = create_qrcode(media_path, "CE KMITL-"+str(quesheet_serializer.data['quesheetid']))
        if data['logo'] != None:
            logo_path = media_path+"logo.jpg"
            fs.save(logo_path, data['logo'])
            chk = create_questionnaire_sheet(media_path, head_1, detail_1, detail_2, part_1, part_2, qrcode=qrcode_path ,logo=logo_path)
        else:
            chk = create_questionnaire_sheet(media_path, head_1, detail_1, detail_2, part_1, part_2, qrcode=qrcode_path)
        if chk == True:
            link_sheet = request.build_absolute_uri("/media"+media+"questionnaire_sheet.jpg")
            val = {"imgquesheet_path": link_sheet}
            quesheet = Quesheet.objects.get(quesheetid=quesheet_serializer.data['quesheetid'])
            serializer = QuesheetSerializer(instance=quesheet, data=val)
            if serializer.is_valid():
                serializer.save()
            return Response({"msg" : "สร้างแบบสอบถามสำเร็จ", "imgquesheet_path" : link_sheet}, status=status.HTTP_201_CREATED)
        else:
            return Response({"err" : chk}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"err" : part_2[1]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def quesheetUpdate(request, pk):
    user = User.objects.get(userid=request.data['userid'])
    quesheet_userid = Quesheet.objects.filter(userid=request.data['userid'])
    if quesheet_userid.count() < user.typesid.limitque:
        data = request.data
        quesheet_data = json.loads(data['quesheet'])
        queheaddetails_data = json.loads(data['queheaddetails'])
        quetopicdetails_data = json.loads(data['quetopicdetails'])
        head_1 = quesheet_data['quesheettopicname']
        detail_1 = quesheet_data['detailslineone']
        detail_2 = quesheet_data['detailslinetwo']
        part_1 = [queheaddetails_data['quehead1'].split(','), 
                queheaddetails_data['quehead2'].split(','), 
                queheaddetails_data['quehead3'].split(','), 
                queheaddetails_data['quehead4'].split(','), 
                queheaddetails_data['quehead5'].split(',')]
        part_2 = chk_validate_qtn(quetopicdetails_data['quetopicdetails'], quetopicdetails_data['quetopicformat'])
        quesheet = Quesheet.objects.get(quesheetid=pk)
        quesheet_serializer = QuesheetSerializer(instance=quesheet, data=quesheet_data)
        if quesheet_serializer.is_valid():
            quesheet_serializer.save()
            queheaddetails = Queheaddetails.objects.get(quesheetid=pk)
            queheaddetails_serializer = QueheaddetailsSerializer(instance=queheaddetails, data=queheaddetails_data)
            if queheaddetails_serializer.is_valid():
                queheaddetails_serializer.save()
                quetopicdetails = Quetopicdetails.objects.get(quesheetid=pk)
                quetopicdetails_serializer = QuetopicdetailsSerializer(instance=quetopicdetails, data=quetopicdetails_data)
                if quetopicdetails_serializer.is_valid():
                    quetopicdetails_serializer.save()
                    fs = FileSystemStorage()
                    media = "/"+str(user.fullname)+"/qtn/"+str(quesheet_serializer.data['quesheetid'])+"/original_sheet/"
                    media_path = fs.path('')+media
                    logo_path = media_path+"logo.jpg"
                    qrcode_path = media_path+"qrcode.jpg"
                    if not os.path.exists(logo_path):
                        chk = create_questionnaire_sheet(media_path, head_1, detail_1, detail_2, part_1, part_2, qrcode=qrcode_path)
                    else:
                        chk = create_questionnaire_sheet(media_path, head_1, detail_1, detail_2, part_1, part_2, qrcode=qrcode_path, logo=logo_path)
                    if chk == True:
                        link_sheet = request.build_absolute_uri("/media"+media+"questionnaire_sheet.jpg")
                        val = {"imgquesheet_path": link_sheet}
                        quesheet = Quesheet.objects.get(quesheetid=quesheet_serializer.data['quesheetid'])
                        quesheet_serializer = QuesheetSerializer(instance=quesheet, data=val)
                        if quesheet_serializer.is_valid():
                            quesheet_serializer.save()
                        return Response({"msg" : "สร้างแบบสอบถามสำเร็จ", "imgquesheet_path" : quesheet_serializer.data['imgquesheet_path']}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"err" : chk}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    queheaddetails_serializer = QueheaddetailsSerializer(instance=queheaddetails_serializer.data, data=queheaddetails)
                    if queheaddetails_serializer.is_valid():
                        queheaddetails_serializer.save()
                    return Response({"err" : queheaddetails_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                quesheet_serializer = QuesheetSerializer(instance=quesheet_serializer.data, data=quesheet)
                if quesheet_serializer.is_valid():
                    quesheet_serializer.save()
                return Response({"err" : quesheet_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(quesheet_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"err" : "จำนวนแบบสอบเกินกำหนดที่สามารถสร้างได้"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def quesheetDelete(request, pk):
    queheaddetails = Queheaddetails.objects.get(quesheetid_head=pk)
    queheaddetails.delete()
    quetopicdetails = Quetopicdetails.objects.get(quesheetid_topic=pk)
    quetopicdetails.delete()
    quesheet = Quesheet.objects.get(quesheetid=pk)
    quesheet.delete()
    fs = FileSystemStorage()
    media = "/"+str(request.data['username'])+"/qtn/"+str(pk)+"/"
    media_path = fs.path('')+media
    if os.path.exists(media_path):
        shutil.rmtree(media_path)
    return Response({"msg" : "ลบแบบสอบถามสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- Queheaddetails
@api_view(['GET'])
def queheaddetailsList(request):
    queryset = Queheaddetails.objects.all().order_by('queheaddetailsid')
    serializer = QueheaddetailsSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def queheaddetailsDetail(request, pk):
    queryset = Queheaddetails.objects.get(queheaddetailsid=pk)
    serializer = QueheaddetailsSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def queheaddetailsCreate(request):
    serializer = QueheaddetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def queheaddetailsUpdate(request, pk):
    queheaddetails = Queheaddetails.objects.get(queheaddetailsid=pk)
    serializer = QueheaddetailsSerializer(instance=queheaddetails, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def queheaddetailsDelete(request, pk):
    queheaddetails = Queheaddetails.objects.get(queheaddetailsid=pk)
    queheaddetails.delete()
    return Response({"msg" : "ลบหัวข้อแบบสอบถามสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- Quetopicdetails
@api_view(['GET'])
def quetopicdetailsList(request):
    queryset = Quetopicdetails.objects.all().order_by('quetopicdetailsid')
    serializer = QuetopicdetailsSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def quetopicdetailsDetail(request, pk):
    queryset = Quetopicdetails.objects.get(quetopicdetailsid=pk)
    serializer = QuetopicdetailsSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def quetopicdetailsCreate(request):
    serializer = QuetopicdetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def quetopicdetailsUpdate(request, pk):
    quetopicdetails = Quetopicdetails.objects.get(quetopicdetailsid=pk)
    serializer = QuetopicdetailsSerializer(instance=quetopicdetails, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def quetopicdetailsDelete(request, pk):
    quetopicdetails = Quetopicdetails.objects.get(quetopicdetailsid=pk)
    quetopicdetails.delete()
    return Response({"msg" : "ลบหัวข้อแบบสอบถามสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- Queinformation
@api_view(['GET'])
def queinformationList(request):
    queryset = Queinformation.objects.all().order_by('queinfoid')
    serializer = QueinformationSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def queinformationDetail(request, pk):
    queryset = Queinformation.objects.get(queinfoid=pk)
    serializer = QueinformationSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def queinformationCreate(request):
    serializer = QueinformationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def queinformationUpdate(request, pk):
    queinformation = Queinformation.objects.get(queinfoid=pk)
    serializer = QueinformationSerializer(instance=queinformation, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def queinformationDelete(request, pk):
    queinformation = Queinformation.objects.get(queinfoid=pk)
    queinformation.delete()
    return Response({"msg" : "ลบข้อมูลแบบสอบถามสำเร็จ"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def queinformationUploadPaper(request):
    res = []
    user = User.objects.get(userid=request.data['userid'])
    quesheet = Quesheet.objects.get(quesheetid=request.data['quesheetid'])
    queheaddetails = Queheaddetails.objects.get(quesheetid=request.data['quesheetid'])
    quetopicdetails = Quetopicdetails.objects.get(quesheetid=request.data['quesheetid'])
    fs = FileSystemStorage()
    default_path = "/"+str(user.fullname)+"/qtn/"+str(request.data['quesheetid'])+"/"
    ori_path = fs.path('')+default_path+"questionnaire/original/"
    pre_path = fs.path('')+default_path+"questionnaire/preprocess/"
    os.makedirs(ori_path, exist_ok=True)
    part_1_path = fs.path('')+default_path+"result/part1/"
    os.makedirs(part_1_path, exist_ok=True)
    part_3_path = fs.path('')+default_path+"result/part3/"
    os.makedirs(part_3_path, exist_ok=True)
    for file in request.FILES.getlist('file'):
        if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg'):
            fs.save(ori_path+file.name, file)
            data = read_qrcode(ori_path+file.name, request.data['src'])
            if data != False:
                pre = pre_process_qtn(ori_path, pre_path, file.name)
                if pre == True:
                    format_part_1 = []
                    part_1 = [queheaddetails.quehead1, queheaddetails.quehead2, queheaddetails.quehead3, queheaddetails.quehead4, queheaddetails.quehead5]
                    for index, i in enumerate(part_1):
                        head = i.split(',')
                        format_part_1.append([])
                        for index_, ii in enumerate(head):
                            format_part_1[-1].append(index_+1)

                    format_part_2 = []
                    part_2 = chk_validate_qtn(quetopicdetails.quetopicdetails, quetopicdetails.quetopicformat)
                    print("part_2 :",part_2)
                    for index, i in enumerate(part_2):
                        if i == "nohead":
                            format_part_2.append([])
                        else:
                            for iindex, ii in enumerate(i):
                                format_part_2.append([])
                                    
                    print("format_part_1 :",format_part_1)
                    print("format_part_2 :",format_part_2)
                    proc = process_qtn(pre_path, part_1_path, part_3_path,"pre_"+file.name, [], format_part_1, format_part_2)
                    print("proc 1 :",proc[1])
                    print("proc 2 :",proc[2])
                    pass
                else:
                    res.append({"err" : pre})
            else:
                res.append({"err" : "ไม่พบ QR Code"})
        else:
            res.append({"err" : "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"})
    return Response(res, status=status.HTTP_201_CREATED)

##########################################################################################
#- Request
@api_view(['GET'])
def requestList(request):
    queryset = Request.objects.all().order_by('requestid')
    serializer = RequestSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def requestDetail(request, pk):
    queryset = Request.objects.get(requestid=pk)
    serializer = RequestSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def requestCreate(request):
    user = User.objects.get(userid=request.data['userid'])
    file = request.FILES['file']
    fs = FileSystemStorage()
    media_path = fs.path('')+"/"+str(user.fullname)+"/request/"
    os.makedirs(media_path, exist_ok=True)
    fs.save(media_path+"request.jpg", file)
    data = request.data
    data['imgrequest_path'] = request.build_absolute_uri("/media/"+str(user.fullname)+"/request/request.jpg")
    data['status_request'] = "Waiting for confirmation"
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def requestUpdate(request, pk):
    request_ = Request.objects.get(requestid=pk)
    serializer = RequestSerializer(instance=request_, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def requestDelete(request, pk):
    request = Request.objects.get(requestid=pk)
    request.delete()
    return Response({"msg" : "ลบคำร้องขอสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- type
@api_view(['GET'])
def typeList(request):
    queryset = Type.objects.all().order_by('typesid')
    serializer = TypeSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def typeDetail(request, pk):
    queryset = Type.objects.get(typesid=pk)
    serializer = TypeSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def typeCreate(request):
    serializer = TypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def typeUpdate(request, pk):
    type = Type.objects.get(typesid=pk)
    serializer = TypeSerializer(instance=type, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def typeDelete(request, pk):
    type = Type.objects.get(typesid=pk)
    type.delete()
    return Response({"msg" : "ลบประเภทผู้ใช้งานสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- subchapter
@api_view(['GET'])
def subchapterList(request):
    queryset = Subchapter.objects.all().order_by('subchapterid')
    serializer = SubchapterSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def subchapterDetail(request, pk):
    queryset = Subchapter.objects.get(subchapterid=pk)
    serializer = SubchapterSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def subchapterCreate(request):
    serializer = SubchapterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def subchapterUpdate(request, pk):
    subchapter = Subchapter.objects.get(subchapterid=pk)
    serializer = SubchapterSerializer(instance=subchapter, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def subchapterDelete(request, pk):
    subchapter = Subchapter.objects.get(subchapterid=pk)
    subchapter.delete()
    return Response({"msg" : "ลบบทย่อยสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- Subject
@api_view(['GET'])
def subjectList(request):
    queryset = Subject.objects.all().order_by('subid')
    serializer = SubjectSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def subjectDetail(request, pk):
    queryset = Subject.objects.get(subid=pk)
    serializer = SubjectSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def subjectCreate(request):
    user = User.objects.get(userid=request.data['userid'])
    subject = Subject.objects.filter(subcode=request.data['userid'])
    if subject.count() < int(user.typesid.limitsubject):
        data = request.data
        data['deletetimesubject'] = None
        data['createtimesubject'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        serializer = SubjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"err" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"err" : "จำนวนวิชาเกินที่กำหนด"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def subjectUpdate(request, pk):
    subject = Subject.objects.get(subid=pk)
    serializer = SubjectSerializer(instance=subject, data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({"err" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def subjectDelete(request, pk):
    subject = Subject.objects.get(subid=pk)
    subject.delete()
    return Response({"msg" : "ลบวิชาสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
