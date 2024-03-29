import pandas as pd
import numpy as np
import csv
import shutil
import os
import json
import math

import time
from datetime import datetime, timedelta

import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

from django.core.files.storage import FileSystemStorage
from django.db.models import Count

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

from .tasks import update_data_task

@api_view(['GET'])
def overview(request):
    api_urls = {
        'update': {
            'PUT-Update': '/update/',
        },
        'user': {
            'GET    - List': '/user/',
            'POST   - Create': '/user/create/',
            'POST   - VerifyEmail': '/verify/email/<str:e_kyc>/',
            'GET    - Detail': '/user/detail/<str:pk>/',
            'PUT    - Update': '/user/update/<str:pk>/',
            'DELETE - Delete': '/user/delete/<str:pk>/',
            'GET    - DuplicateEmail': '/user/duplicate/email/<str:email>/',
            'GET    - DuplicateGoogleid': '/user/duplicate/googleid/<str:googleid>/',
            'POST   - Login': '/user/login/',
            'POST   - LoginGoogle': '/user/login/google/',
        },
        'exam': {
            'GET    - List': '/exam/',
            'POST   - Create': '/exam/create/',
            'GET    - Detail': '/exam/detail/<str:pk>/',
            'GET    - DetailBySubid': '/exam/detail/subject/<str:pk>/',
            'PUT    - Update': '/exam/update/<str:pk>/',
            'DELETE - Delete': '/exam/delete/<str:pk>/',
            'POST   - UploadCSV': '/exam/upload/csv/',
            'POST   - UploadLogo': '/exam/upload/logo/',
            'GET    - SendScore' : '/exam/sendmail/<str:pk>'
        },
        'examanswers': {
            'GET    - List': '/examanswers/',
            'POST   - Create': '/examanswers/create/',
            'GET    - Detail': '/examanswers/detail/<str:pk>/',
            'GET    - DetailByExamid': '/examanswers/detail/examid/<str:pk>/',
            'PUT    - Update': '/examanswers/update/<str:pk>/',
            'DELETE - Delete': '/examanswers/delete/<str:pk>/',
            'POST   - UploadPaper': '/examanswers/upload/paper/',
        },
        'examinformation': {
            'GET    - List': '/examinformation/',
            'POST   - Create': '/examinformation/create/',
            'GET    - Detail': '/examinformation/detail/<str:pk>/',
            'GET    - DetailByExamid': '/examinformation/detail/exam/<str:pk>/',
            'GET    - DetailByEmail': '/examinformation/detail/email/<str:pk>/',
            'PUT    - Update': '/examinformation/update/<str:pk>/',
            'DELETE - Delete': '/examinformation/delete/<str:pk>/',
            'POST   - UploadPaper': '/examinformation/upload/paper/',
            'GET    - TableAns': '/examinformation/tableans/<str:pk>/',
            'POST   - Result': '/examinformation/result/<str:pk>/',
        },
        'chapter': {
            'GET    - List': '/chapter/',
            'POST   - Create': '/chapter/create/',
            'GET    - Detail': '/chapter/detail/<str:pk>/',
            'GET    - DtailByUserid': '/chapter/detail/user/<str:pk>/',
            'PUT    - Update': '/chapter/update/<str:pk>/',
            'DELETE - Delete': '/chapter/delete/<str:pk>/',
        },
        'chapteranswer': {
            'GET    - List': '/chapteranswer/',
            'POST   - Create': '/chapteranswer/create/',
            'GET    - Detail': '/chapteranswer/detail/<str:pk>/',
            'GET    - DetailByChapterid': '/chapteranswer/detail/chapter/<str:pk>/',
            'PUT    - Update': '/chapteranswer/update/<str:pk>/',
            'DELETE - Delete': '/chapteranswer/delete/<str:pk>/',
        },
        'queheaddetails': {
            'GET    - List': '/queheaddetails/',
            'POST   - Create': '/queheaddetails/create/',
            'GET    - Detail': '/queheaddetails/detail/<str:pk>/',
            'PUT    - Update': '/queheaddetails/update/<str:pk>/',
            'DELETE - Delete': '/queheaddetails/delete/<str:pk>/',
        },
        'quesheet': {
            'GET    - List': '/quesheet/',
            'POST   - Create': '/quesheet/create/',
            'GET    - Detail': '/quesheet/detail/<str:pk>/',
            'GET    - DetailByUserid': '/quesheet/detail/user/<str:pk>/',
            'PUT    - Update': '/quesheet/update/<str:pk>/',
            'DELETE - Delete': '/quesheet/delete/<str:pk>/',
        },
        'quetopicdetails': {
            'GET    - List': '/quetopicdetails/',
            'POST   - Create': '/quetopicdetails/create/',
            'GET    - Detail': '/quetopicdetails/detail/<str:pk>/',
            'PUT    - Update': '/quetopicdetails/update/<str:pk>/',
            'DELETE - Delete': '/quetopicdetails/delete/<str:pk>/',
        },
        'queinformation': {
            'GET    - List': '/queinformation/',
            'POST   - Create': '/queinformation/create/',
            'GET    - Detail': '/queinformation/detail/<str:pk>/',
            'PUT    - Update': '/queinformation/update/<str:pk>/',
            'DELETE - Delete': '/queinformation/delete/<str:pk>/',
            'POST   - UploadPaper': '/queinformation/upload/paper/',
            'POST   - Result': '/queinformation/result/<str:pk>/',
        },
        'request': {
            'GET    - List': '/request/',
            'POST   - Create': '/request/create/',
            'GET    - Detail': '/request/detail/<str:pk>/',
            'GET    - DetailByUserid' : '/request/detail/user/<str:pk>/',
            'PUT    - Update': '/request/update/<str:pk>/',
            'DELETE - Delete': '/request/delete/<str:pk>/',
        },
        'subchapter': {
            'GET    - List': '/subchapter/',
            'POST   - Create': '/subchapter/create/',
            'GET    - Detail': '/subchapter/detail/<str:pk>/',
            'GET    - DetailByChapterid': '/subchapter/detail/chapter/<str:pk>/',
            'PUT    - Update': '/subchapter/update/<str:pk>/',
            'DELETE - Delete': '/subchapter/delete/<str:pk>/',
        },
        'subject': {
            'GET    - List': '/subject/',
            'POST   - Create': '/subject/create/',
            'GET    - Detail': '/subject/detail/<str:pk>/',
            'GET    - DetailByUserid': '/subject/detail/user/<str:pk>/',
            'PUT    - Update': '/subject/update/<str:pk>/',
            'DELETE - Delete': '/subject/delete/<str:pk>/',
        },
        'type': {
            'GET    - List': '/type/',
            'POST   - Create': '/type/create/',
            'GET    - Detail': '/type/detail/<str:pk>/',
            'PUT    - Update': '/type/update/<str:pk>/',
            'DELETE - Delete': '/type/delete/<str:pk>/',
        },
    }
    return Response(api_urls)

##########################################################################################
#- Method
def setDatetime(day):
    datetime_ = datetime.now() + timedelta(days=day)
    datetime_ = datetime_.replace(hour=23, minute=59, second=59)
    datetime_ = datetime.strftime(datetime_, "%Y-%m-%dT%H:%M:%S+07:00")
    return datetime_

#- Sendmail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
def sendmail(subject, message, recipient_list):
    send_mail(subject, 
              message, 
              settings.EMAIL_HOST_USER, 
              recipient_list)
    return True
##########################################################################################
#- Update
@api_view(['PUT'])
def update(request):
    update_data_task()
    return Response({"msg" : "อัปเดตสำเร็จ"}, status=status.HTTP_200_OK)
##########################################################################################
#- User
user_notfound = {"err" : "ไม่พบข้อมูลผู้ใช้งาน"}
@api_view(['GET'])
def userList(request):
    try:
        queryset = User.objects.all().order_by('-userid')
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def userDetail(request, pk):
    try:
        queryset = User.objects.get(userid=pk)
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def userCreate(request):
    data = request.data
    salt, hashed_password = hash_password(data['password'])
    data['password'] = hashed_password
    data['salt'] = salt
    data['createtimeuser'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00")

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        if 'googleid' not in data or data['googleid'] == '':
            sendmail("ยืนยันอีเมลบัญชี MCQAS", 
                     f"สวัสดี, คุณ {data['fullname']}\nคลิกลิงค์นี้เพื่อทำการยืนยันอีเมลบัญชี MCQAS : {request.data['url']}verify/{data['e_kyc']}/", 
                     [data['email']])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"err" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def userVerifyEmail(request, e_kyc):
    try:
        user = User.objects.get(e_kyc=e_kyc)
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    data = {"e_kyc" : "1"}
    serializer = UserSerializer(instance=user, data=data)
    if serializer.is_valid():
        serializer.save()
    return Response({"msg" : "ยืนยันอีเมลสำเร็จ"}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def userUpdate(request, pk):
    try:
        user = User.objects.get(userid=pk)
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    data = request.data
    if 'password' in request.data:
        salt, hashed_password = hash_password(data['password'])
        data['password'] = hashed_password
        data['salt'] = salt
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def userDelete(request, pk):
    try:
        user = User.objects.get(userid=pk)
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({"msg" : "ลบผู้ใช้งานสำเร็จ"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def userDuplicateEmail(request, email):
    queryset = User.objects.filter(email=email).count()
    if queryset == 0:
        return Response(True)
    else:
        return Response({"err" : "Email มีผู้ใช้งานแล้ว"}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def userDuplicateGoogleid(request, googleid):
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
    if email == '' or email == None or password == '' or password == None:
        return Response({"err" : "กรุณากรอกอีเมล และรหัสผ่าน"}, status=status.HTTP_400_BAD_REQUEST)
    if queryset.count() > 0:
        if queryset[0].e_kyc == '1':
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
                return Response({"err" : "อีเมลหรือรหัสผ่านไม่ถูกต้อง"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"err" : "อีเมลนี้ยังไม่ได้ทำการยืนยัน กรุณาตรวจสอบเมลเพื่อทำการยืนยัน"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"err" : "ไม่พบอีเมลนี้ในระบบ"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def userLoginGoogle(request):
    googleid = request.data['googleid']
    queryset = User.objects.filter(googleid=googleid, e_kyc='1')
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
#- Subject
subject_notfound = {"err" : "ไม่พบข้อมูลวิชา"}
@api_view(['GET'])
def subjectList(request):
    try:
        queryset = Subject.objects.all().order_by('-subid')
    except Subject.DoesNotExist:
        return Response(subject_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SubjectSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def subjectDetail(request, pk):
    try:
        queryset = Subject.objects.get(subid=pk)
    except Subject.DoesNotExist:
        return Response(subject_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SubjectSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def subjectDetailByUserid(request, pk):
    try:
        queryset = Subject.objects.filter(userid=pk, statussubject="1")
    except Subject.DoesNotExist:
        return Response(subject_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SubjectSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def subjectCreate(request):
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    subject = Subject.objects.filter(userid=request.data['userid'], statussubject="1")
    if subject.count() < int(user.typesid.limitsubject):
        data = request.data
        data['statussubject'] = "1"
        data['deletetimesubject'] = None
        data['createtimesubject'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00")
        serializer = SubjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"err" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"err" : "จำนวนวิชาเกินที่กำหนด"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
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
    try:
        subject = Subject.objects.get(subid=pk)
    except Subject.DoesNotExist:
        return Response(subject_notfound, status=status.HTTP_400_BAD_REQUEST)
    
    data = {"deletetimesubject" : setDatetime(7)}
    serializer = SubjectSerializer(instance=subject, data=data)
    if serializer.is_valid():
        serializer.save()
    return Response({"msg" : "วิชาจะถูกลบในวันที่และเวลา", "deletetime": data['deletetimesubject']}, status=status.HTTP_200_OK)

##########################################################################################
#- Exam
exam_notfound = {"err" : "ไม่พบข้อมูลข้อสอบ"}
@api_view(['GET'])
def examList(request):
    try:
        queryset = Exam.objects.all().order_by('-examid')
    except Exam.DoesNotExist:
        return Response(exam_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExamSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def examDetail(request, pk):
    try:
        queryset = Exam.objects.get(examid=pk)
    except Exam.DoesNotExist:
        return Response(exam_notfound, status=status.HTTP_404_NOT_FOUND)
    serializer = ExamSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def examDetailBySubid(request, pk):
    try:
        queryset = Exam.objects.filter(subid=pk, statusexam='1').order_by("-examid")
    except Exam.DoesNotExist:
        return Response(exam_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExamSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def examCreate(request):
    data = request.data
    data['answersheetformat'] = '1'
    data['imganswersheetformat_path'] = request.build_absolute_uri("/media/original_answersheet/")
    data['statusexam'] = '1'
    data['deletetimeexam'] = None
    data['createtimeexam'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00")
    exam = Exam.objects.filter(subid=data['subid'], statusexam='1')
    user = User.objects.get(userid=data['userid'])
    if exam.count() < user.typesid.limitexam:
        serializer = ExamSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"err" : "จำนวนข้อสอบของรายวิชานี้เกินที่กำหนด"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def examUpdate(request, pk):
    data = request.data
    if 'reset_logo' in request.data:
        data['imganswersheetformat_path'] = request.build_absolute_uri("/media/original_answersheet/")
    try:
        exam = Exam.objects.get(examid=pk)
    except Exam.DoesNotExist:
        return Response(exam_notfound, status=status.HTTP_404_NOT_FOUND)
    serializer = ExamSerializer(instance=exam, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def examDelete(request, pk):
    try:
        exam = Exam.objects.get(examid=pk)
    except Exam.DoesNotExist:
        return Response(exam_notfound, status=status.HTTP_404_NOT_FOUND)
    
    data = {"deletetimeexam" : setDatetime(7)}
    serializer = ExamSerializer(instance=exam, data=data)
    if serializer.is_valid():
        serializer.save()
    return Response({"msg" : "การสอบจะถูกลบในวันที่และเวลา", "deletetime" : data['deletetimeexam']}, status=status.HTTP_200_OK)

@api_view(['POST'])
def examUploadCSV(request):
    file = request.FILES['file']
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    if file.name.endswith('.csv'):
        exam = Exam.objects.get(examid=request.data['examid'])
        fs = FileSystemStorage()
        media = "/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(exam.examid)+"/student_list/"
        media_path = fs.path('')+media
        os.makedirs(media_path, exist_ok=True)
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
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg') or file.name.lower().endswith('.png'):
        exam = Exam.objects.get(examid=request.data['examid'])
        fs = FileSystemStorage()
        media = "/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(exam.examid)+"/answersheet_format/"
        media_path = fs.path('')+media
        os.makedirs(media_path, exist_ok=True)
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

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
@api_view(['GET'])
def examSendMail(request, pk):
    fs = FileSystemStorage()
    try:
        exam = Exam.objects.select_related("subid").get(examid=pk)
    except Exam.DoesNotExist:
        return Response(exam_notfound, status=status.HTTP_404_NOT_FOUND)
    examindfo = Examinformation.objects.filter(examid=pk)
    for info in examindfo:
        if info.stdemail != None or info.stdemail != "" or info.stdemail != "nan":
            examanswers = Examanswers.objects.get(examid=pk, examnoanswers=info.setexaminfo)
            chk = chk_ans(info.anschoicestd, exam.numberofexams, examanswers.choiceanswers, examanswers.scoringcriteria)
            data = {
                'subject_name': exam.subid.subjectname,
                'subject_id': exam.subid.subjectid,
                'exam_name': exam.examname,
                'exam_no': info.setexaminfo,
                'student_id': info.stdid,
                'score': info.score,
                'maxscore': chk[3]
            }
            # Render the HTML template with the data
            html_content = render_to_string(fs.path('templates/score.html'), {'data': data})

            # Compose the email
            subject = 'Exam Results'
            from_email = settings.EMAIL_HOST_USER
            to_email = [info.stdemail]

            try:
                # Create the EmailMessage object
                msg = EmailMultiAlternatives(subject, strip_tags(html_content), from_email, to_email)
                msg.attach_alternative(html_content, "text/html")

                # Send the email
                msg.send()
            except Exception as e:
                # Handle exceptions
                # print(f"Error sending email to {to_email}: {str(e)}")
                pass
            
    exam.sendemail = 2
    exam.save()
    return Response({"ok": True}, status=status.HTTP_200_OK)

##########################################################################################
#- Examanswers
examanswers_notfound = {"err" : "ไม่พบข้อมูลเฉลยข้อสอบ"}
@api_view(['GET'])
def examanswersList(request):
    try:
        queryset = Examanswers.objects.all().order_by('-examanswersid')
    except Examanswers.DoesNotExist:
        return Response(examanswers_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExamanswersSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def examanswersDetail(request, pk):
    try:
        queryset = Examanswers.objects.get(examanswersid=pk)
    except Examanswers.DoesNotExist:
        return Response(examanswers_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExamanswersSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def examanswersDetailByExamid(request, pk):
    try:
        queryset = Examanswers.objects.filter(examid=pk)
    except Examanswers.DoesNotExist:
        return Response(examanswers_notfound, status=status.HTTP_404_NOT_FOUND)
    serializer = ExamanswersSerializer(queryset, many=True)
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
    

@api_view(['PUT'])
def examanswersUpdate(request, pk):
    examanswers = Examanswers.objects.get(examanswersid=pk)
    serializer = ExamanswersSerializer(instance=examanswers, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def examanswersDelete(request, pk):
    try:
        examanswers = Examanswers.objects.get(examanswersid=pk)
    except Examanswers.DoesNotExist:
        return Response(examanswers_notfound, status=status.HTTP_404_NOT_FOUND)
    
    examanswers.delete()
    return Response({"msg" : "ลบเฉลยข้อสอบสำเร็จ"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def examanswersUploadPaper(request):
    file = request.FILES['file']
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    exam = Exam.objects.get(examid=request.data['examid'])
    if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg') or file.name.lower().endswith('.png'):
        answers_ = ''
        fs = FileSystemStorage()
        media = "/"+str(user.userid)+"/ans/temp/"
        media_path = fs.path('')+media
        original_path = media_path+"original/"
        os.makedirs(original_path, exist_ok=True)
        save_file_path = fs.save(original_path+file.name, file)

        preprocess_path = media_path+"preprocess/"
        os.makedirs(preprocess_path, exist_ok=True)
        pre = pre_process_ans(original_path, preprocess_path, save_file_path.split("/")[-1])
        if pre == True:
            pre_img_name = "pre_"+save_file_path.split("/")[-1].split(".")[0]+".jpg"
            data = process_ans(preprocess_path, pre_img_name, exam.numberofexams, debug=False)
            err = ''
            for i in range(0, len(data[0])):
                if data[0][i] != None:
                    err += str(data[0][i])+"\n"
            if err == '':
                for i in range(0, len(data[6])):
                    if i != 0: answers_ += ','
                    for ii in range(1, len(data[6][i])):
                        if ii == 1:
                            answers_ += str(data[6][i][ii])
                        elif ii != 1:
                            answers_ += ':'+str(data[6][i][ii])
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
examinformation_notfound = {"err" : "ไม่พบข้อมูลข้อสอบ"}
@api_view(['GET'])
def examinformationList(request):
    try:
        queryset = Examinformation.objects.all().order_by('-examinfoid')
    except Examinformation.DoesNotExist:
        return Response(examinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExaminformationSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def examinformationDetail(request, pk):
    try:
        queryset = Examinformation.objects.get(examinfoid=pk)
    except Examinformation.DoesNotExist:
        return Response(examinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExaminformationSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def examinformationDetailByExamid(request, pk):
    try:
        queryset = Examinformation.objects.filter(examid=pk)
    except Examinformation.DoesNotExist:
        return Response(examinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    
    duplicate_stdid = queryset.values('stdid').annotate(stdid_count=Count('stdid')).filter(stdid_count__gt=1)
    # Filter queryset to include only records with duplicate stdid
    queryset_duplicate = queryset.filter(stdid__in=[item['stdid'] for item in duplicate_stdid])
    # Serialize data for records with duplicate stdid
    serializer_duplicate = ExaminformationSerializer(queryset_duplicate, many=True)
    # Serialize data for records without duplicate stdid
    queryset_non_duplicate = queryset.exclude(stdid__in=[item['stdid'] for item in duplicate_stdid])
    serializer_non_duplicate = ExaminformationSerializer(queryset_non_duplicate, many=True)

    # Return both sets of data
    return Response({
        'duplicate_records': serializer_duplicate.data,
        'non_duplicate_records': serializer_non_duplicate.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def examinformationDetailByEmail(request, pk):
    try:
        queryset = Examinformation.objects.filter(stdemail=pk, examid__showscores=1).order_by("-examinfoid")
    except Examinformation.DoesNotExist:
        return Response(examinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExaminformationSerializer(queryset, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def examinformationCreate(request):
    serializer = ExaminformationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def examinformationUpdate(request, pk):
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    exam = Exam.objects.get(examid=request.data['examid'])
    examinformation = Examinformation.objects.get(examinfoid=pk)
    file = request.FILES['file'] if 'file' in request.FILES else None
    if file == None:
        data = request.data
        data_ = {}
        data_['stdid'] = data['stdid']
        data_['subjectidstd'] = data['subjectidstd']
        data_['setexaminfo'] = data['setexaminfo']
        data_['examid'] = data['examid']

        fs = FileSystemStorage()
        csv_path = fs.path('')+"/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(request.data['examid'])+"/student_list/student_list.csv"
        df = pd.read_csv(csv_path)
        df['รหัสนักศึกษา'] = df['รหัสนักศึกษา'].astype(str)
        index = df[df['รหัสนักศึกษา'] == data['stdid']].index
        data_["errorstype"] = "ไม่พบรหัสนักศึกษาในรายชื่อ" if index.empty else ''
        data_['stdemail'] = df['อีเมล'][index[0]] if not index.empty else None

        if examinformation.setexaminfo != data_['setexaminfo']:
            try:
                examanswers = Examanswers.objects.get(examid=data_['examid'], examnoanswers=data_['setexaminfo'])
            except Examanswers.DoesNotExist:
                return Response({"err" : "ไม่พบเฉลยข้อสอบ"}, status=status.HTTP_404_NOT_FOUND)
            ans = chk_ans(examinformation.anschoicestd, exam.numberofexams, examanswers.choiceanswers, examanswers.scoringcriteria)
            data_['score'] = ans[4]
            data_['correct'] = ans[5]
            data_['wrong'] = ans[6]
            data_['unresponsive'] = ans[8]
            data_['itemanalysis'] = ans[9]
            data_['errorstype'] = ans[0]
        serializer = ExaminformationSerializer(instance=examinformation, data=data_)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # print("File")
        fs = FileSystemStorage()
        default_path = "/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(request.data['examid'])+"/answersheet/"
        ori_path = fs.path('')+default_path+"original/"
        pre_path = fs.path('')+default_path+"preprocess/"
        pre_path_ = "/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(request.data['examid'])+"/answersheet/preprocess/"
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
        if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg') or file.name.lower().endswith('.png'):
            old_img = examinformation.imgansstd_path.split("/")[-1]
            old_img = old_img.replace("pre_", "", 1)
            if os.path.exists(ori_path+old_img):
                os.remove(ori_path+old_img)
            if os.path.exists(pre_path+"pre_"+old_img):
                os.remove(pre_path+"pre_"+old_img)
            if os.path.exists(pre_path+"table_ans_detect/table_ans_pre_"+old_img):
                os.remove(pre_path+"table_ans_detect/table_ans_pre_"+old_img)
            save_file_path = fs.save(ori_path+file.name, file)
            img_link = request.build_absolute_uri("/media/"+save_file_path)
            pre = pre_process_ans(ori_path, pre_path, save_file_path.split("/")[-1])
            examinfo['imgansstd_path'] = img_link

            if pre == True:
                pre_img_name = "pre_"+save_file_path.split("/")[-1].split(".")[0]+".jpg"
                img_link = request.build_absolute_uri("/media"+default_path+"preprocess/"+pre_img_name)
                examinfo['imgansstd_path'] = img_link
                data = process_ans(pre_path, pre_img_name, exam.numberofexams, debug=False)
                error_data = ''
                for i in range(0, len(data[0])):
                    if data[0][i] != None:
                        if error_data == '':
                            error_data += str(data[0][i])
                        else:
                            error_data += ','+str(data[0][i])
                if data[0][2] != "ไม่พบ Marker ของส่วนคำตอบ":
                    # chk_validate_ans return [check, std_id, sec, seat_id, sub_id, ex_id, answer]
                    valid = chk_validate_ans(data[1], data[2], data[3], data[4], data[5], data[6])
                    error_valid = ''
                    for i in range(0, len(valid[0])):
                        if valid[0][i] != None:
                            if error_valid == '':
                                error_valid += str(valid[0][i])
                            else:
                                error_valid += ','+str(valid[0][i])
                    examinfo['stdid'] = valid[1]
                    examinfo['section'] = valid[2]
                    examinfo['examseatnumber'] = valid[3]
                    examinfo['subjectidstd'] = valid[4]
                    if valid[5] == '' : valid[5] = None
                    examinfo['setexaminfo'] = valid[5]
                    examinfo['anschoicestd'] = valid[6]
                    examinfo['errorstype'] = error_valid if error_valid != '' else None

                    csv_path = fs.path('')+"/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(request.data['examid'])+"/student_list/student_list.csv"
                    df = pd.read_csv(csv_path)
                    df['รหัสนักศึกษา'] = df['รหัสนักศึกษา'].astype(str)
                    index = df[df['รหัสนักศึกษา'] == valid[1]].index
                    err_std = "ไม่พบรหัสนักศึกษาในรายชื่อ" if index.empty else ''
                    examinfo['stdemail'] = df['อีเมล'][index[0]] if not index.empty else None

                    try:
                        queryset = Examanswers.objects.get(examid=request.data['examid'], examnoanswers=valid[5])
                        examanswers_serializer = ExamanswersSerializer(queryset, many=False)
                    except Examanswers.DoesNotExist:
                        examanswers_serializer = None
                    
                    if examanswers_serializer != None:
                        # chk_ans return [error, ans, chans, max_score, score, right, wrong, rightperchoice, notans, analys]
                        ans = chk_ans(valid[6], exam.numberofexams, examanswers_serializer.data['choiceanswers'], examanswers_serializer.data['scoringcriteria'])
                        examinfo['score'] = ans[4]
                        examinfo['correct'] = ans[5]
                        examinfo['wrong'] = ans[6]
                        examinfo['unresponsive'] = ans[8]
                        examinfo['itemanalysis'] = ans[9]
                        if examinfo['errorstype'] == None:
                            if ans[0] == '' and err_std == '':
                                examinfo['errorstype'] = None
                            elif ans[0] != '' and err_std == '':
                                examinfo['errorstype'] = ans[0]
                            elif ans[0] == '' and err_std != '':
                                examinfo['errorstype'] = err_std
                            else :
                                examinfo['errorstype'] = err_std+","+ans[0]
                        else:
                            if ans[0] != '' and err_std == '':
                                examinfo['errorstype'] += ','+ans[0]
                            elif ans[0] == '' and err_std != '':
                                examinfo['errorstype'] += ','+err_std
                            elif ans[0] != '' and err_std != '':
                                examinfo['errorstype'] += ','+err_std+","+ans[0]
                    else :
                        err_set = "ไม่พบข้อมูลเฉลยข้อสอบ"
                        examinfo['errorstype'] = err_set if err_std == '' else err_set+","+err_std
                else:
                    examinfo['errorstype'] = error_data
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
    try:
        examinformation = Examinformation.objects.get(examinfoid=pk)
    except Examinformation.DoesNotExist:
        return Response(examinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    
    examinformation.delete()
    return Response({"msg" : "ลบข้อมูลข้อสอบสำเร็จ"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def examinformationUploadPaper(request):
    # tic = time.time()
    res = []
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    exam = Exam.objects.get(examid=request.data['examid'])
    fs = FileSystemStorage()
    default_path = "/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(request.data['examid'])+"/answersheet/"
    ori_path = fs.path('')+default_path+"original/"
    pre_path = fs.path('')+default_path+"preprocess/"
    pre_path_ = "/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(request.data['examid'])+"/answersheet/"+"preprocess/"
    os.makedirs(ori_path, exist_ok=True)

    for file in request.FILES.getlist('file'):
        examinfo = {
            "examid" : request.data['examid']
        }
        if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg') or file.name.lower().endswith('.png'):
            save_file_path = fs.save(ori_path+file.name, file)
            img_link = request.build_absolute_uri("/media/"+save_file_path)
            examinfo['imgansstd_path'] = img_link
            pre = pre_process_ans(ori_path, pre_path, save_file_path.split("/")[-1])

            if pre == True:
                pre_img_name = "pre_"+save_file_path.split("/")[-1].split(".")[0]+".jpg"
                img_link = request.build_absolute_uri("/media"+default_path+"preprocess/"+pre_img_name)
                examinfo['imgansstd_path'] = img_link
                data = process_ans(pre_path, pre_img_name, exam.numberofexams, debug=False)
                # print(data)
                error_data = ''
                for i in range(0, len(data[0])):
                    if data[0][i] != None:
                        if error_data == '':
                            error_data += str(data[0][i])
                        else:
                            error_data += ','+str(data[0][i])
                if data[0][2] != "ไม่พบ Marker ของส่วนคำตอบ":
                    # chk_validate_ans return [check, std_id, sec, seat_id, sub_id, ex_id, answer]
                    valid = chk_validate_ans(data[1], data[2], data[3], data[4], data[5], data[6])
                    error_valid = ''
                    for i in range(0, len(valid[0])):
                        if valid[0][i] != None:
                            if error_valid == '':
                                error_valid += str(valid[0][i])
                            else:
                                error_valid += ','+str(valid[0][i])
                    examinfo['stdid'] = valid[1]
                    examinfo['section'] = valid[2]
                    examinfo['examseatnumber'] = valid[3]
                    examinfo['subjectidstd'] = valid[4]
                    if valid[5] == '' : valid[5] = None
                    examinfo['setexaminfo'] = valid[5]
                    examinfo['anschoicestd'] = valid[6]
                    examinfo['errorstype'] = error_valid if error_valid != '' else None

                    csv_path = fs.path('')+"/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(request.data['examid'])+"/student_list/student_list.csv"
                    df = pd.read_csv(csv_path)
                    df['รหัสนักศึกษา'] = df['รหัสนักศึกษา'].astype(str)
                    index = df[df['รหัสนักศึกษา'] == valid[1]].index
                    err_std = "ไม่พบรหัสนักศึกษาในรายชื่อ" if index.empty else ''
                    examinfo['stdemail'] = df['อีเมล'][index[0]] if not index.empty else None

                    try:
                        queryset = Examanswers.objects.get(examid=request.data['examid'], examnoanswers=valid[5])
                        examanswers_serializer = ExamanswersSerializer(queryset, many=False)
                    except Examanswers.DoesNotExist:
                        examanswers_serializer = None
                    
                    if examanswers_serializer != None:
                        # chk_ans return [error, ans, chans, max_score, score, right, wrong, rightperchoice, notans, analys]
                        ans = chk_ans(valid[6], exam.numberofexams, examanswers_serializer.data['choiceanswers'], examanswers_serializer.data['scoringcriteria'])
                        examinfo['score'] = ans[4]
                        examinfo['correct'] = ans[5]
                        examinfo['wrong'] = ans[6]
                        examinfo['unresponsive'] = ans[8]
                        examinfo['itemanalysis'] = ans[9]
                        if examinfo['errorstype'] == None:
                            if ans[0] == '' and err_std == '':
                                examinfo['errorstype'] = None
                            elif ans[0] != '' and err_std == '':
                                examinfo['errorstype'] = ans[0]
                            elif ans[0] == '' and err_std != '':
                                examinfo['errorstype'] = err_std
                            else :
                                examinfo['errorstype'] = err_std+","+ans[0]
                        else:
                            if ans[0] != '' and err_std == '':
                                examinfo['errorstype'] += ','+ans[0]
                            elif ans[0] == '' and err_std != '':
                                examinfo['errorstype'] += ','+err_std
                            elif ans[0] != '' and err_std != '':
                                examinfo['errorstype'] += ','+err_std+","+ans[0]
                    else :
                        err_set = "ไม่พบข้อมูลเฉลยข้อสอบ"
                        examinfo['errorstype'] = err_set if err_std == '' else err_set+","+err_std
                else:
                    examinfo['errorstype'] = error_data
            else:
                examinfo['errorstype'] = pre
        else:
            examinfo['errorstype'] = "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"

        examinfo['createtimeexaminfo'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00")
        examinfo_serializer = ExaminformationSerializer(data=examinfo)
        if examinfo_serializer.is_valid():
            examinfo_serializer.save()
        else:
            # print("examinfo_serializer.errors : ", examinfo_serializer.errors)
            pass
        res.append(examinfo_serializer.data)
    res_dict = {"result" : res}
    # toc = time.time()
    # print("Time: ", toc-tic)
    # print("res: ", len(res_dict['result']))
    exam.sequencesteps = '4'
    exam.save()
    return Response(res_dict, status=status.HTTP_201_CREATED)

from urllib.parse import unquote
@api_view(['GET'])
def examinformationTableAns(request, pk):
    try:
        examinfo = Examinformation.objects.get(examinfoid=pk)
    except Examinformation.DoesNotExist:
        return Response(examinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    fs = FileSystemStorage()
    imgansstd_path = unquote(examinfo.imgansstd_path)
    examinfo_file_path = imgansstd_path.split('/')[4:]
    examinfo_file_path[-1] = "table_ans_"+examinfo_file_path[-1]
    examinfo_file_path[-2] += "/table_ans_detect"
    table_ans_path = "/"+"/".join(examinfo_file_path)
    fs_table_ans_path = fs.path('')+table_ans_path
    # print(fs_table_ans_path)
    if os.path.exists(fs_table_ans_path) == False:
        examinfo_file_path = examinfo.imgansstd_path.split('/')[4:]
        pre_path = fs.path('')+"/"+"/".join(examinfo_file_path[0:-1])+"/"
        file_name = unquote(examinfo_file_path[-1])
        exam = Exam.objects.get(examid=examinfo_file_path[3])
        data = process_ans(pre_path, file_name, exam.numberofexams, debug=True)
        if data[0][2] == None:
            return Response({"msg": "วาดตารางสำเร็จ", "img_path": request.build_absolute_uri("/media"+table_ans_path)}, status=status.HTTP_200_OK)
        else:
            return Response({"err": "ไม่พบตารางคำตอบ"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"msg": "วาดตารางสำเร็จ", "img_path": request.build_absolute_uri("/media"+table_ans_path)}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def examinformationResult(request, pk):
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    try:
        exam = Exam.objects.get(examid=pk)
    except Exam.DoesNotExist:
        return Response(exam_notfound, status=status.HTTP_404_NOT_FOUND)
    queryset = Examinformation.objects.filter(examid=pk).order_by('-score')
    examinfo_serializer = ExaminformationSerializer(queryset, many=True)
    fs = FileSystemStorage()
    csv_path = fs.path('')+"/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(exam.examid)+"/student_list/student_list.csv"
    if os.path.exists(csv_path):
        # Result Score
        csv_result_path = fs.path('')+"/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(exam.examid)+"/result/"
        os.makedirs(csv_result_path, exist_ok=True)
        csv_result_path += "result_student_list.csv"
        # Copy the original file to the result directory with a new name
        shutil.copyfile(csv_path, os.path.join(csv_result_path))

        data_proc = [
            ['', '', 'Min :'],
            ['', '', 'Max :'],
            ['', '', 'Average :'],
            ['', '', 'Median :'],
            ['', '', 'Variance :'],
            ['', '', 'S.D :'],
            ['', '', 'C.V.(%) :'],
            ['', '', 'Total :'],
        ]

        # Read the CSV file into a list of lists
        inFile = []
        with open(csv_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                inFile.append(row.copy())

        # Find and remove the column named 'อีเมล' if it exists
        if 'อีเมล' in inFile[0]:
            column_to_remove_index = inFile[0].index('อีเมล')
            for row in inFile:
                del row[column_to_remove_index]

        # Add new columns to the header row
        inFile[0].extend(['จำนวนข้อที่ตอบถูก', 'จำนวนข้อที่ตอบผิด', 'จำนวนข้อที่ไม่ตอบ', 'คะแนน'])

        # Add data_proc to inFile
        inFile.extend(data_proc)

        correct = []
        wrong = []
        no_ans = []
        score = []

        data_row = [correct, wrong, no_ans, score]

        for i in examinfo_serializer.data:
            for ii in inFile[1:]:
                if ii[0] == i['stdid']:
                    ii.extend([i['correct'], 
                                i['wrong'], 
                                i['unresponsive'], 
                                i['score']])
                    data_row[0].append(int(i['correct']))
                    data_row[1].append(int(i['wrong']))
                    data_row[2].append(int(i['unresponsive']))
                    data_row[3].append(float(i['score']))

        for i in range(len(data_row)):
            data_proc[0].append(np.min(data_row[i]))
            data_proc[1].append(np.max(data_row[i]))
            data_proc[2].append(round(np.average(data_row[i]), 2))
            data_proc[3].append(round(np.median(data_row[i]), 2))
            data_proc[4].append(round(np.var(data_row[i]), 2))
            data_proc[5].append(round(np.std(data_row[i]), 2))
            data_proc[6].append(round(np.std(data_row[i])/np.average(data_row[i])*100, 2))
            data_proc[7].append(np.sum(data_row[i]))

        # Write the updated data back to the CSV file
        with open(csv_result_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            for row in inFile:
                writer.writerow(row)
        result_csv_path = request.build_absolute_uri("/media/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(exam.examid)+"/result/result_student_list.csv")
        
        analysis_csv_path_list = []
        for i in range(int(exam.numberofexamsets)):
            queryset = Examinformation.objects.filter(examid=pk, setexaminfo=i+1).order_by('-score')
            examinfo_serializer = ExaminformationSerializer(queryset, many=True)
            # Analysis Data
            data = [["ข้อที่", "ค่าความยาก", "แปลผลค่าความยาก", "ค่าอำนาจจำแนก", "แปลผลค่าอำนาจจำแนก"]]
            if len(examinfo_serializer.data) > 30: num_group = math.ceil(len(examinfo_serializer.data)/100*27)
            else: num_group = math.ceil(len(examinfo_serializer.data)/2)
            analys = [item['itemanalysis'].split(',') for item in examinfo_serializer.data]
            for ii in range(int(exam.numberofexams)):
                choice_data = []
                difficulty = 0
                discrimination = 0
                high_group = 0
                low_group = 0
                choice_data.append(ii+1)
                for iii in range(len(analys)):
                    difficulty += int(analys[iii][ii])
                    if iii < num_group: high_group += int(analys[iii][ii])
                    elif iii >= len(analys)-num_group: low_group += int(analys[iii][ii])

                if len(examinfo_serializer.data) != 0:
                    difficulty = round(difficulty/len(examinfo_serializer.data), 2)
                    choice_data.append(difficulty)
                    if difficulty < 0.2: choice_data.append("ยากมาก")
                    elif difficulty < 0.4: choice_data.append("ค่อนข้างยาก")
                    elif difficulty < 0.6: choice_data.append("ยากพอเหมาะ")
                    elif difficulty < 0.8: choice_data.append("ค่อนข้างง่าย")
                    else: choice_data.append("ง่ายมาก")

                    discrimination = round((high_group-low_group)/(num_group*2), 2)
                    choice_data.append(discrimination)
                    if discrimination < 0: choice_data.append("จำแนกไม่ได้")
                    elif discrimination < 0.2: choice_data.append("จำแนกไม่ค่อยได้")
                    elif discrimination < 0.4: choice_data.append("จำแนกได้บ้าง")
                    elif discrimination < 0.6: choice_data.append("จำแนกได้ปานกลาง")
                    elif discrimination < 0.8: choice_data.append("จำแนกดี")
                    elif discrimination < 1: choice_data.append("จำแนกดีมาก")
                    else: choice_data.append("จำแนกดีเลิศ")

                    data.append(choice_data)

            fs = FileSystemStorage()
            csv_itemanalysis_path = fs.path('')+"/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(exam.examid)+"/result/item_analysis_ชุดที่_"+str(i+1)+".csv"
            # Write the data to the CSV file
            with open(csv_itemanalysis_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                for row in data:
                    writer.writerow(row)
            analysis_csv_path = request.build_absolute_uri("/media/"+str(user.userid)+"/ans/"+str(exam.subid.subid)+"/"+str(exam.examid)+"/result/item_analysis_ชุดที่_"+str(i+1)+".csv")
            analysis_csv_path_list.append(analysis_csv_path)
        
        analysis_csv_path = ",".join(analysis_csv_path_list)
        exam.result_csv_path = result_csv_path
        exam.analysis_csv_path = analysis_csv_path
        exam.sequencesteps = '6'
        exam.save()
        return Response({"msg" : "วิเคราะห์ผลเสร็จสิ้น"}, status=status.HTTP_200_OK)
    else:
        return Response({"err" : "ไม่พบไฟล์รายชื่อนักศึกษา"}, status=status.HTTP_404_NOT_FOUND)

##########################################################################################
#- Quesheet
quesheet_notfound = {"err" : "ไม่พบข้อมูลแบบสอบถาม"}
@api_view(['GET'])
def quesheetList(request):
    try:
        queryset = Quesheet.objects.all().order_by('-quesheetid')
    except Quesheet.DoesNotExist:
        return Response(quesheet_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QuesheetSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def quesheetDetail(request, pk):
    try:
        queryset = Quesheet.objects.get(quesheetid=pk)
    except Quesheet.DoesNotExist:
        return Response(quesheet_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QuesheetSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def quesheetDetailByUserid(request, pk):
    try:
        queryset = Quesheet.objects.filter(userid=pk, statusquesheet='1').order_by("-quesheetid")
    except Quesheet.DoesNotExist:
        return Response(quesheet_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QuesheetSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def quesheetCreate(request):
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    quesheet_userid = Quesheet.objects.filter(userid=request.data['userid'], statusquesheet='1')
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
        for c, i in enumerate(part_1):
            for cc, ii in enumerate(i):
                if ii == 'อื่นๆ': part_1[c][cc] += '__________'
        part_2 = chk_part_2_qtn(quetopicdetails_data['quetopicdetails'], quetopicdetails_data['quetopicformat'])
        if part_2[0] != False:
            quesheet_data['statusquesheet'] = '1'
            quesheet_data['createtimequesheet'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00")
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
            media = "/"+str(user.userid)+"/qtn/"+str(quesheet_serializer.data['quesheetid'])+"/original_sheet/"
            media_path = fs.path('')+media
            os.makedirs(media_path, exist_ok=True)
            for filename in os.listdir(media_path):
                if os.path.isfile(os.path.join(media_path, filename)):
                    os.remove(os.path.join(media_path, filename))
            qrcode_path = create_qrcode(media_path, "CE KMITL-"+str(quesheet_serializer.data['quesheetid']))
            if 'logo' in request.FILES:
                logo_path = media_path+"logo.jpg"
                fs.save(logo_path, request.FILES['logo'])
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
            return Response({"err" : part_2[1], "err_": part_2[2]}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"err" : "จำนวนแบบสอบถามเกินกำหนดที่สามารถสร้างได้"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def quesheetUpdate(request, pk):
    data = request.data
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    if 'datetimestart' in request.data or 'datetimeend' in request.data or 'deletetimequesheet' in request.data or 'sequencesteps' in request.data:
        data = request.data
        quesheet = Quesheet.objects.get(quesheetid=pk, userid=user.userid)
        serializer = QuesheetSerializer(instance=quesheet, data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
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
        for c, i in enumerate(part_1):
            for cc, ii in enumerate(i):
                if ii == 'อื่นๆ': part_1[c][cc] += '__________'
        part_2 = chk_part_2_qtn(quetopicdetails_data['quetopicdetails'], quetopicdetails_data['quetopicformat'])
        if part_2[0] != False:
            quesheet = Quesheet.objects.get(quesheetid=pk, userid=user.userid)
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
                        media = "/"+str(user.userid)+"/qtn/"+str(quesheet_serializer.data['quesheetid'])+"/original_sheet/"
                        media_path = fs.path('')+media
                        logo_path = media_path+"logo.jpg"
                        qrcode_path = media_path+"qrcode.jpg"
                        if 'logo' in request.FILES and (data['nonelogo'] == False or data['nonelogo'] == "false"):
                            if os.path.exists(logo_path):
                                os.remove(logo_path)
                            fs.save(logo_path, request.FILES['logo'])
                            chk = create_questionnaire_sheet(media_path, head_1, detail_1, detail_2, part_1, part_2, qrcode=qrcode_path ,logo=logo_path)
                        elif os.path.exists(logo_path) and (data['nonelogo'] == False or data['nonelogo'] == "false"):
                            chk = create_questionnaire_sheet(media_path, head_1, detail_1, detail_2, part_1, part_2, qrcode=qrcode_path ,logo=logo_path)
                        else:
                            if os.path.exists(logo_path):
                                os.remove(logo_path)
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
                        quetopicdetails_serializer = QuetopicdetailsSerializer(instance=quetopicdetails_serializer.data, data=queheaddetails)
                        if quetopicdetails_serializer.is_valid():
                            quetopicdetails_serializer.save()
                        return Response({"err" : quetopicdetails_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    queheaddetails_serializer = QueheaddetailsSerializer(instance=queheaddetails_serializer.data, data=quetopicdetails)
                    if queheaddetails_serializer.is_valid():
                        queheaddetails_serializer.save()
                    return Response({"err" : queheaddetails_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                quesheet_serializer = QuesheetSerializer(instance=quesheet_serializer.data, data=quesheet)
                if quesheet_serializer.is_valid():
                    quesheet_serializer.save()
            return Response({"err" : quesheet_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)   
        else:
            return Response({"err" : part_2[1], "err_": part_2[2]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def quesheetDelete(request, pk):
    try:
        quesheet = Quesheet.objects.get(quesheetid=pk)
    except Quesheet.DoesNotExist:
        return Response(quesheet_notfound, status=status.HTTP_404_NOT_FOUND)
    
    data = {'deletetimequesheet' : setDatetime(7)}
    serializer = QuesheetSerializer(instance=quesheet, data=data)
    if serializer.is_valid():
        serializer.save()
    return Response({"msg" : "แบบสอบถามจะถูกลบในวันที่และเวลา", "deletetime" : data['deletetimequesheet']}, status=status.HTTP_200_OK)

##########################################################################################
#- Queheaddetails
@api_view(['GET'])
def queheaddetailsList(request):
    queryset = Queheaddetails.objects.all().order_by('-queheaddetailsid')
    serializer = QueheaddetailsSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def queheaddetailsDetail(request, pk):
    queryset = Queheaddetails.objects.get(quesheetid=pk)
    serializer = QueheaddetailsSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def queheaddetailsCreate(request):
    serializer = QueheaddetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
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
    queryset = Quetopicdetails.objects.all().order_by('-quetopicdetailsid')
    serializer = QuetopicdetailsSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def quetopicdetailsDetail(request, pk):
    queryset = Quetopicdetails.objects.get(quesheetid=pk)
    serializer = QuetopicdetailsSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def quetopicdetailsCreate(request):
    serializer = QuetopicdetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
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
queinformation_notfound = {"err" : "ไม่พบข้อมูลแบบสอบถาม"}
@api_view(['GET'])
def queinformationList(request):
    try:
        queryset = Queinformation.objects.all().order_by('-queinfoid')
    except Queinformation.DoesNotExist:
        return Response(queinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QueinformationSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def queinformationDetail(request, pk):
    try:
        queryset = Queinformation.objects.get(queinfoid=pk)
    except Queinformation.DoesNotExist:
        return Response(queinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QueinformationSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def queinformationDetailByQuesheetid(request, pk):
    try:
        queryset = Queinformation.objects.filter(quesheetid=pk).order_by('-queinfoid')
    except Queinformation.DoesNotExist:
        return Response(queinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QueinformationSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def queinformationCreate(request):
    serializer = QueinformationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def queinformationUpdate(request, pk):
    try:
        queinformation = Queinformation.objects.get(queinfoid=pk)
    except Queinformation.DoesNotExist:
        return Response(queinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    file = request.FILES['file'] if 'file' in request.FILES else None
    if file == None:
        queinformation_update = request.data
        serializer = QueinformationSerializer(instance=queinformation, data=queinformation_update)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        try:
            user = User.objects.get(userid=request.data['userid'])
        except User.DoesNotExist:
            return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
        try:
            quesheet = Quesheet.objects.get(quesheetid=request.data['quesheetid'])
            queheaddetails = Queheaddetails.objects.get(quesheetid=request.data['quesheetid'])
            quetopicdetails = Quetopicdetails.objects.get(quesheetid=request.data['quesheetid'])
        except Quesheet.DoesNotExist:
            return Response(quesheet_notfound, status=status.HTTP_404_NOT_FOUND)
        
        quehead = [queheaddetails.quehead1, 
                   queheaddetails.quehead2, 
                   queheaddetails.quehead3, 
                   queheaddetails.quehead4, 
                   queheaddetails.quehead5]
        p1_answer_format = []
        for c, i in enumerate(quehead):
            i = i.split(',')
            for cc, ii in enumerate(i):
                if ii == 'อื่นๆ':
                    p1_answer_format.append("p1"+str(c+1)+str(cc))

        fs = FileSystemStorage()
        default_path = "/"+str(user.userid)+"/qtn/"+str(request.data['quesheetid'])+"/"
        ori_path = fs.path('')+default_path+"questionnaire/original/"
        pre_path = fs.path('')+default_path+"questionnaire/preprocess/"
        part_1_path = fs.path('')+default_path+"result/part1/"
        part_3_path = fs.path('')+default_path+"result/part3/"

        queinformation_data = {
            "quesheetid" : request.data['quesheetid'],
            "ansquehead" : None,
            "ansquetopic" : None,
            "ansother": None,
            "additionalsuggestions": None,
            "imgansstd_path" : None,
            "status_queinfo" : "Offline",
            "errorstype" : None
        }

        if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg') or file.name.lower().endswith('.png'):
            old_img = queinformation.imgansstd_path.split("/")[-1]
            old_img = old_img.replace("pre_", "", 1)
            if os.path.exists(ori_path+old_img):
                os.remove(ori_path+old_img)
            if os.path.exists(pre_path+"pre_"+old_img):
                os.remove(pre_path+"pre_"+old_img)
            if os.path.exists(part_3_path+"p3_pre_"+old_img):
                os.remove(part_3_path+"p3_pre_"+old_img)
            save_file_path = fs.save(ori_path+file.name, file)
            img_link = request.build_absolute_uri("/media/"+save_file_path)
            queinformation_data['imgansstd_path'] = img_link
            pre = pre_process_qtn(ori_path, pre_path, save_file_path.split("/")[-1])
            if pre == True:
                pre_img_name = "pre_"+save_file_path.split("/")[-1].split(".")[0]+".jpg"
                img_link = request.build_absolute_uri("/media"+default_path+"questionnaire/preprocess/"+pre_img_name)
                queinformation_data['imgansstd_path'] = img_link

                format_part_1 = []
                part_1 = [queheaddetails.quehead1, queheaddetails.quehead2, queheaddetails.quehead3, queheaddetails.quehead4, queheaddetails.quehead5]
                for index, i in enumerate(part_1):
                    head = i.split(',')
                    format_part_1.append([])
                    for index_, ii in enumerate(head):
                        format_part_1[-1].append(index_+1)

                format_part_2 = []
                part_2 = chk_part_2_qtn(quetopicdetails.quetopicdetails, quetopicdetails.quetopicformat)
                for index, i in enumerate(part_2):
                    if i == "nohead":
                        format_part_2.append([])
                    else:
                        for iindex, ii in enumerate(i):
                            format_part_2.append([])

                proc = process_qtn(pre_path, part_1_path, part_3_path, pre_img_name, p1_answer_format, format_part_1, format_part_2)
                if proc[0][0]:
                    valid = chk_validate_qtn(proc[1], proc[2])
                    queinformation_data['ansquehead'] = valid[1]
                    queinformation_data['ansquetopic'] = valid[2]

                    for i in range(len(proc[3])):
                        if proc[3][i] != "":
                            proc[3][i] = request.build_absolute_uri("/media"+default_path+"result/part1/"+proc[3][i])
                    queinformation_data['ansother'] = ",".join(proc[3])

                    if proc[4] != None:
                        queinformation_data['additionalsuggestions'] = request.build_absolute_uri("/media"+default_path+"result/part3/"+str(proc[4]))

                    if os.path.exists(pre_path+pre_img_name) == True:
                        data = read_qrcode(pre_path+pre_img_name)
                    else:
                        data = read_qrcode(ori_path+save_file_path.split("/")[-1])

                    if data != "CE KMITL-"+str(request.data['quesheetid']) and data != False:
                        queinformation_data['errorstype'] = "QR Code ไม่ตรงกับแบบสอบถาม"
                    elif data == False:
                        queinformation_data['errorstype'] = "ไม่พบข้อมูล QR Code ในแบบสอบถาม"

                    if valid[0][0] == False:
                        if queinformation_data['errorstype'] != None:
                            queinformation_data['errorstype'] += ","
                            if valid[0][1] != None and valid[0][2] != None:
                                queinformation_data['errorstype'] += str(valid[0][1])+","+str(valid[0][2])
                            elif valid[0][1] != None and valid[0][2] == None:
                                queinformation_data['errorstype'] += valid[0][1]
                            elif valid[0][1] == None and valid[0][2] != None:
                                queinformation_data['errorstype'] += valid[0][2]
                        else:
                            if valid[0][1] != None and valid[0][2] != None:
                                queinformation_data['errorstype'] = str(valid[0][1])+","+str(valid[0][2])
                            elif valid[0][1] != None and valid[0][2] == None:
                                queinformation_data['errorstype'] = valid[0][1]
                            elif valid[0][1] == None and valid[0][2] != None:
                                queinformation_data['errorstype'] = valid[0][2]
                else:
                    if proc[0][1] != None and proc[0][2] != None:
                        queinformation_data['errorstype'] = str(proc[0][1])+","+str(proc[0][2])
                    elif proc[0][1] != None and proc[0][2] == None:
                        queinformation_data['errorstype'] = proc[0][1]
                    elif proc[0][1] == None and proc[0][2] != None:
                        queinformation_data['errorstype'] = proc[0][2]
            else:
                queinformation_data['errorstype'] = pre
        else:
            return Response({"err" : "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"}, status=status.HTTP_400_BAD_REQUEST)

        queinformation_serializer = QueinformationSerializer(instance=queinformation, data=queinformation_data)
        if queinformation_serializer.is_valid():
            queinformation_serializer.save()
        return Response(queinformation_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def queinformationDelete(request, pk):
    try:
        queinformation = Queinformation.objects.get(queinfoid=pk)
    except Queinformation.DoesNotExist:
        return Response(queinformation_notfound, status=status.HTTP_404_NOT_FOUND)
    
    queinformation.delete()
    return Response({"msg" : "ลบข้อมูลแบบสอบถามสำเร็จ"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def queinformationUploadPaper(request):
    tic = time.time()
    res = []
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    try:
        quesheet = Quesheet.objects.get(quesheetid=request.data['quesheetid'])
        queheaddetails = Queheaddetails.objects.get(quesheetid=request.data['quesheetid'])
        quetopicdetails = Quetopicdetails.objects.get(quesheetid=request.data['quesheetid'])
    except Quesheet.DoesNotExist:
        return Response(quesheet_notfound, status=status.HTTP_404_NOT_FOUND)

    quehead = [queheaddetails.quehead1, 
               queheaddetails.quehead2, 
               queheaddetails.quehead3, 
               queheaddetails.quehead4, 
               queheaddetails.quehead5]
    p1_answer_format = []
    for c, i in enumerate(quehead):
        i = i.split(',')
        for cc, ii in enumerate(i):
            if ii == 'อื่นๆ':
                p1_answer_format.append("p1"+str(c+1)+str(cc))
                
    fs = FileSystemStorage()
    default_path = "/"+str(user.userid)+"/qtn/"+str(request.data['quesheetid'])+"/"
    ori_path = fs.path('')+default_path+"questionnaire/original/"
    pre_path = fs.path('')+default_path+"questionnaire/preprocess/"
    os.makedirs(ori_path, exist_ok=True)
    part_1_path = fs.path('')+default_path+"result/part1/"
    os.makedirs(part_1_path, exist_ok=True)
    part_3_path = fs.path('')+default_path+"result/part3/"
    os.makedirs(part_3_path, exist_ok=True)
    for file in request.FILES.getlist('file'):
        queinformation_data = {
            "quesheetid" : request.data['quesheetid'],
            "ansquehead" : None,
            "ansquetopic" : None,
            "ansother": None,
            "additionalsuggestions": None,
            "imgansstd_path" : None,
            "status_queinfo" : "Offline",
            "errorstype" : None
        }
        if file.name.lower().endswith('.jpg') or file.name.lower().endswith('.jpeg') or file.name.lower().endswith('.png'):
            save_file_path = fs.save(ori_path+file.name, file)
            img_link = request.build_absolute_uri("/media/"+save_file_path)
            queinformation_data['imgansstd_path'] = img_link
            pre = pre_process_qtn(ori_path, pre_path, save_file_path.split("/")[-1])
            if pre == True:
                pre_img_name = "pre_"+save_file_path.split("/")[-1].split(".")[0]+".jpg"
                img_link = request.build_absolute_uri("/media"+default_path+"questionnaire/preprocess/"+pre_img_name)
                queinformation_data['imgansstd_path'] = img_link

                format_part_1 = []
                part_1 = [queheaddetails.quehead1, queheaddetails.quehead2, queheaddetails.quehead3, queheaddetails.quehead4, queheaddetails.quehead5]
                for index, i in enumerate(part_1):
                    head = i.split(',')
                    format_part_1.append([])
                    for index_, ii in enumerate(head):
                        format_part_1[-1].append(index_+1)

                format_part_2 = []
                part_2 = chk_part_2_qtn(quetopicdetails.quetopicdetails, quetopicdetails.quetopicformat)
                for index, i in enumerate(part_2):
                    if i == "nohead":
                        format_part_2.append([])
                    else:
                        for iindex, ii in enumerate(i):
                            format_part_2.append([])

                proc = process_qtn(pre_path, part_1_path, part_3_path, pre_img_name, p1_answer_format, format_part_1, format_part_2)

                if proc[0][0]:
                    # print("proc : ", proc)
                    valid = chk_validate_qtn(proc[1], proc[2])
                    # print("valid : ", valid)
                    queinformation_data['ansquehead'] = valid[1]
                    queinformation_data['ansquetopic'] = valid[2]

                    for i in range(len(proc[3])):
                        if proc[3][i] != "":
                            proc[3][i] = request.build_absolute_uri("/media"+default_path+"result/part1/"+proc[3][i])
                    queinformation_data['ansother'] = ",".join(proc[3])

                    if proc[4] != None:
                        queinformation_data['additionalsuggestions'] = request.build_absolute_uri("/media"+default_path+"result/part3/"+str(proc[4]))

                    if os.path.exists(pre_path+pre_img_name) == True:
                        data = read_qrcode(pre_path+pre_img_name)
                    else:
                        data = read_qrcode(ori_path+save_file_path.split("/")[-1])

                    if data != "CE KMITL-"+str(request.data['quesheetid']) and data != False:
                        queinformation_data['errorstype'] = "QR Code ไม่ตรงกับแบบสอบถาม"
                    elif data == False:
                        queinformation_data['errorstype'] = "ไม่พบข้อมูล QR Code ในแบบสอบถาม"

                    if valid[0][0] == False:
                        if queinformation_data['errorstype'] != None:
                            queinformation_data['errorstype'] += ","
                            if valid[0][1] != None and valid[0][2] != None:
                                queinformation_data['errorstype'] += str(valid[0][1])+","+str(valid[0][2])
                            elif valid[0][1] != None and valid[0][2] == None:
                                queinformation_data['errorstype'] += valid[0][1]
                            elif valid[0][1] == None and valid[0][2] != None:
                                queinformation_data['errorstype'] += valid[0][2]
                        else:
                            if valid[0][1] != None and valid[0][2] != None:
                                queinformation_data['errorstype'] = str(valid[0][1])+","+str(valid[0][2])
                            elif valid[0][1] != None and valid[0][2] == None:
                                queinformation_data['errorstype'] = valid[0][1]
                            elif valid[0][1] == None and valid[0][2] != None:
                                queinformation_data['errorstype'] = valid[0][2]
                else:
                    if proc[0][1] != None and proc[0][2] != None:
                        queinformation_data['errorstype'] = str(proc[0][1])+","+str(proc[0][2])
                    elif proc[0][1] != None and proc[0][2] == None:
                        queinformation_data['errorstype'] = proc[0][1]
                    elif proc[0][1] == None and proc[0][2] != None:
                        queinformation_data['errorstype'] = proc[0][2]
            else:
                queinformation_data['errorstype'] = pre
        else:
            queinformation_data['errorstype'] = "สกุลไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .jpg"
        queinformation_data['createtimequesheetinfo'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00")
        queinformation_serializer = QueinformationSerializer(data=queinformation_data)
        if queinformation_serializer.is_valid():
            queinformation_serializer.save()
        # else:
        #     print("queinformation_serializer.errors : ", queinformation_serializer.errors)
        res.append(queinformation_serializer.data)
    quesheet.sequencesteps = '3'
    quesheet.save()
    result = {"msg" : "อัพโหลดข้อมูลแบบสอบถามสำเร็จ", "result" : res}
    toc = time.time()
    # print("Time : ", toc-tic)
    # print("Result : ", len(result['result']))
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def queinformationResult(request, pk):
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    try:
        quesheet = Quesheet.objects.get(quesheetid=pk)
        queheaddetails = Queheaddetails.objects.get(quesheetid=pk)
        quetopicdetails = Quetopicdetails.objects.get(quesheetid=pk)
    except Quesheet.DoesNotExist:
        return Response(quesheet_notfound, status=status.HTTP_404_NOT_FOUND)
    queryset = Queinformation.objects.filter(quesheetid=pk)
    queinfo_serializer = QueinformationSerializer(queryset, many=True)
    fs = FileSystemStorage()
    csv_result_path = fs.path('')+"/"+str(user.userid)+"/qtn/"+str(quesheet.quesheetid)+"/result/"
    os.makedirs(csv_result_path, exist_ok=True)
    status_list = ['Offline', 'Online', 'All']
    csv_result_part1_list = []
    csv_result_part2_list = []
    for stat in status_list:
        if stat == 'All' and len(csv_result_part1_list) == 1: break
        if stat == 'All':
            queryset = Queinformation.objects.filter(quesheetid=pk)
            queinfo_serializer = QueinformationSerializer(queryset, many=True)
        else:
            queryset = Queinformation.objects.filter(quesheetid=pk, status_queinfo=stat)
            queinfo_serializer = QueinformationSerializer(queryset, many=True)

        if len(queinfo_serializer.data) > 0:
            csv_result_part1_path = csv_result_path+"result_part1_"+str(stat)+".csv"

            data_row_part1 = [[0] * 6 for _ in range(5)]
            for index, i in enumerate(queinfo_serializer.data):
                i['ansquehead'].split(",")
                for iindex, ii in enumerate(i['ansquehead'].split(",")):
                    if ii != 'n':
                        data_row_part1[iindex][int(ii)-1] += 1
                        data_row_part1[iindex][-1] += 1
                    
            quehead_list = [queheaddetails.quehead1.split(','),
                            queheaddetails.quehead2.split(','),
                            queheaddetails.quehead3.split(','),
                            queheaddetails.quehead4.split(','),
                            queheaddetails.quehead5.split(',')]
            part1_data = []
            for i in range(len(quehead_list)):
                for ii in range(len(quehead_list[i])):
                    pass_ = False
                    if ii == 0 and quehead_list[i][ii] != '':
                        part1_data.append([quehead_list[i][ii], "จำนวน",  "%"])
                    elif ii != 0 and quehead_list[i][ii] != '':
                        part1_data.append([quehead_list[i][ii], data_row_part1[i][ii-1], round(data_row_part1[i][ii-1]/data_row_part1[i][-1]*100, 2)])
                    elif ii == 0 and quehead_list[i][ii] == '':
                        pass_ = True
                        break
                if pass_ == False:
                    part1_data.append(["รวม", data_row_part1[i][-1], round(data_row_part1[i][-1]/data_row_part1[i][-1]*100, 2)])

            with open(csv_result_part1_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                for row in part1_data:
                    writer.writerow(row)
            resultpart1_csv_path = request.build_absolute_uri("/media/"+str(user.userid)+"/qtn/"+str(quesheet.quesheetid)+"/result/result_part1_"+str(stat)+".csv")
            csv_result_part1_list.append(resultpart1_csv_path)

            csv_result_part2_path = csv_result_path+"result_part2_"+str(stat)+".csv"
            part2_data = [["หัวข้อการประเมิน", 
                        "มากที่สุด(5)",
                        "มาก(4)",
                        "ปานกลาง(3)",
                        "น้อย(2)",
                        "น้อยที่สุด(1)",
                        "ไม่ประเมิน(0)",
                        "จำนวนผู้ประเมิน",
                        "ค่าเฉลี่ย",
                        "ค่าเฉลี่ย(%)",
                        "ส่วนเบี่ยงเบนมาตรฐาน",
                        "ระดับความพึงพอใจ"]]
            
            data_for_summary = [[] for _ in range(10)]
            data_row_part2 = [[0] * 12 for _ in range(18)]
            quetopic = quetopicdetails.quetopicdetails.split(',')
            quetopic_format = quetopicdetails.quetopicformat.split(',')
            ansquetopic = [item['ansquetopic'].split(',') for item in queinfo_serializer.data]
            for i in range(len(quetopic)):
                data_row_part2[i][0] = quetopic[i]
                if quetopic_format[i] == '0':
                    if quetopic[i] != '':
                        for ii in range(len(ansquetopic)):
                            if ansquetopic[ii][i] != 'n':
                                data_row_part2[i][6-int(ansquetopic[ii][i])] += 1
                                data_row_part2[i][8] += int(ansquetopic[ii][i])
                            else:
                                data_row_part2[i][6] += 1

                        data_for_summary[0].append(data_row_part2[i][1]) # 5
                        data_for_summary[1].append(data_row_part2[i][2]) # 4
                        data_for_summary[2].append(data_row_part2[i][3]) # 3
                        data_for_summary[3].append(data_row_part2[i][4]) # 2
                        data_for_summary[4].append(data_row_part2[i][5]) # 1
                        data_for_summary[5].append(data_row_part2[i][6]) # 0

                        data_row_part2[i][7] = np.sum(data_row_part2[i][1:7]) # Sum
                        data_for_summary[6].append(data_row_part2[i][7]) # Sum

                        data_row_part2[i][8] = round(data_row_part2[i][8]/data_row_part2[i][7], 2) # Average
                        data_for_summary[7].append(data_row_part2[i][8]) # Average

                        data_row_part2[i][9] = data_row_part2[i][8]*100/5 # Average %
                        data_for_summary[8].append(data_row_part2[i][9]) # Average %

                        data_row_part2[i][10] = round(np.std(data_row_part2[i][1:7]), 2) # std
                        data_for_summary[9].append(data_row_part2[i][10]) # std

                        # Interpret Results
                        if data_row_part2[i][8] < 1.51: data_row_part2[i][11] = "น้อย" 
                        elif data_row_part2[i][8] < 2.51: data_row_part2[i][11] = "น้อยที่สุด"
                        elif data_row_part2[i][8] < 3.51: data_row_part2[i][11] = "ปานกลาง"
                        elif data_row_part2[i][8] < 4.51: data_row_part2[i][11] = "มาก"
                        else: data_row_part2[i][11] = "มากที่สุด"
                    else:
                        data_row_part2[i][::] = ''
                else:
                    data_row_part2[i][1:] = ''
                part2_data.append(data_row_part2[i][::])

            part2_data = [lst for lst in part2_data if lst]

            summary = ['รวม',
                    np.sum(data_for_summary[0]),
                    np.sum(data_for_summary[1]),
                    np.sum(data_for_summary[2]),
                    np.sum(data_for_summary[3]),
                    np.sum(data_for_summary[4]),
                    np.sum(data_for_summary[5]),
                    np.sum(data_for_summary[6]),
                    round(np.average(data_for_summary[7]), 2),
                    round(np.average(data_for_summary[8]), 2),
                    round(np.average(data_for_summary[9]), 2)]
            if summary[8] < 1.51: summary.append("น้อย")
            elif summary[8] < 2.51: summary.append("น้อยที่สุด")
            elif summary[8] < 3.51: summary.append("ปานกลาง")
            elif summary[8] < 4.51: summary.append("มาก")
            else: summary.append("มากที่สุด")
            part2_data.append(summary)

            with open(csv_result_part2_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                for row in part2_data:
                    writer.writerow(row)
            resultpart2_csv_path = request.build_absolute_uri("/media/"+str(user.userid)+"/qtn/"+str(quesheet.quesheetid)+"/result/result_part2_"+str(stat)+".csv")
            csv_result_part2_list.append(resultpart2_csv_path)

    quesheet.resultpart1_csv_path = ",".join(csv_result_part1_list)
    quesheet.resultpart2_csv_path = ",".join(csv_result_part2_list)
    quesheet.sequencesteps = '5'
    quesheet.save()
    return Response({"msg" : "วิเคราะห์ผลเสร็จสิ้น"}, status=status.HTTP_201_CREATED)

##########################################################################################
#- Request
request_notfound = {"err" : "ไม่พบข้อมูลคำร้องขอ"}
@api_view(['GET'])
def requestList(request):
    try:
        queryset = Request.objects.all().order_by('-requestid')
    except Request.DoesNotExist:
        return Response(request_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = RequestSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def requestDetail(request, pk):
    try:
        queryset = Request.objects.get(requestid=pk)
    except Request.DoesNotExist:
        return Response(request_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = RequestSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def requestDetailByUserid(request, pk):
    queryset = Request.objects.filter(userid=pk)
    if queryset.count() != 0:
        serializer = RequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(request_notfound, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def requestCreate(request):
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    request_indb = Request.objects.filter(userid=request.data['userid'])
    file = request.FILES['file']
    fs = FileSystemStorage()
    media_path = fs.path('')+"/"+str(user.userid)+"/request/"
    os.makedirs(media_path, exist_ok=True)
    save_file_path = fs.save(media_path+"request.jpg", file)
    data = request.data
    data['imgrequest_path'] = request.build_absolute_uri("/media/"+save_file_path)
    data['status_request'] = "1"
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def requestUpdate(request, pk):
    try:
        user = User.objects.get(userid=request.data['userid'])
    except User.DoesNotExist:
        return Response(user_notfound, status=status.HTTP_404_NOT_FOUND)
    request_ = Request.objects.get(requestid=pk)
    data = request.data
    if 'file' in request.FILES:
        file = request.FILES['file']
        fs = FileSystemStorage()
        media_path = fs.path('')+"/"+str(user.userid)+"/request/"
        os.makedirs(media_path, exist_ok=True)
        save_file_path = fs.save(media_path+"request.jpg", file)
        data['imgrequest_path'] = request.build_absolute_uri("/media/"+save_file_path)
    serializer = RequestSerializer(instance=request_, data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def requestDelete(request, pk):
    try:
        request_ = Request.objects.get(requestid=pk)
    except Request.DoesNotExist:
        return Response(request_notfound, status=status.HTTP_404_NOT_FOUND)
    
    request_.delete()
    return Response({"msg" : "ลบคำร้องขอสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- type
type_notfound = {"err" : "ไม่พบข้อมูลประเภทผู้ใช้งาน"}
@api_view(['GET'])
def typeList(request):
    try:
        queryset = Type.objects.all().order_by('-typesid')
    except Type.DoesNotExist:
        return Response(type_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TypeSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def typeDetail(request, pk):
    try:
        queryset = Type.objects.get(typesid=pk)
    except Type.DoesNotExist:
        return Response(type_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TypeSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def typeCreate(request):
    serializer = TypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def typeUpdate(request, pk):
    type = Type.objects.get(typesid=pk)
    serializer = TypeSerializer(instance=type, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def typeDelete(request, pk):
    try:
        type = Type.objects.get(typesid=pk)
    except Type.DoesNotExist:
        return Response(type_notfound, status=status.HTTP_404_NOT_FOUND)
    
    type.delete()
    return Response({"msg" : "ลบประเภทผู้ใช้งานสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- chapter
chapter_notfound = {"err" : "ไม่พบข้อมูลบทเรียน"}
@api_view(['GET'])
def chapterList(request):
    try:
        queryset = Chapter.objects.all().order_by('-chapterid')
    except Chapter.DoesNotExist:
        return Response(chapter_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChapterSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def chapterDetail(request, pk):
    try:
        queryset = Chapter.objects.get(chapterid=pk)
    except Chapter.DoesNotExist:
        return Response(chapter_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChapterSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def chapterDetailByUserid(request, pk):
    try:
        queryset = Chapter.objects.filter(userid=pk)
    except Chapter.DoesNotExist:
        return Response(chapter_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChapterSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def chapterCreate(request):
    serializer = ChapterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def chapterUpdate(request, pk):
    chapter = Chapter.objects.get(chapterid=pk)
    serializer = ChapterSerializer(instance=chapter, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def chapterDelete(request, pk):
    try:
        chapter = Chapter.objects.get(chapterid=pk)
    except Chapter.DoesNotExist:
        return Response(chapter_notfound, status=status.HTTP_404_NOT_FOUND)
    chapter.delete()
    return Response({"msg" : "ลบบทเรียนสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- subchapter
subchapter_notfound = {"err" : "ไม่พบข้อมูลบทย่อย"}
@api_view(['GET'])
def subchapterList(request):
    try:
        queryset = Subchapter.objects.all().order_by('-subchapterid')
    except Subchapter.DoesNotExist:
        return Response(subchapter_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SubchapterSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def subchapterDetail(request, pk):
    try:
        queryset = Subchapter.objects.get(subchapterid=pk)
    except Subchapter.DoesNotExist:
        return Response(subchapter_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SubchapterSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def subchapterDetailByChapterid(request, pk):
    try:
        queryset = Subchapter.objects.filter(chapterid=pk)
    except Subchapter.DoesNotExist:
        return Response(subchapter_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SubchapterSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def subchapterCreate(request):
    serializer = SubchapterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def subchapterUpdate(request, pk):
    subchapter = Subchapter.objects.get(subchapterid=pk)
    serializer = SubchapterSerializer(instance=subchapter, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def subchapterDelete(request, pk):
    try:
        subchapter = Subchapter.objects.get(subchapterid=pk)
    except Subchapter.DoesNotExist:
        return Response(subchapter_notfound, status=status.HTTP_404_NOT_FOUND)
    
    subchapter.delete()
    return Response({"msg" : "ลบบทย่อยสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################
#- chapteranswer
chapteranswer_notfound = {"err" : "ไม่พบข้อมูลคำตอบของบทเรียน"}
@api_view(['GET'])
def chapteranswerList(request):
    try:
        queryset = Chapteranswer.objects.all().order_by('-chapteranswerid')
    except Chapteranswer.DoesNotExist:
        return Response(chapteranswer_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChapteranswerSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def chapteranswerDetail(request, pk):
    try:
        queryset = Chapteranswer.objects.get(chapteranswerid=pk)
    except Chapteranswer.DoesNotExist:
        return Response(chapteranswer_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChapteranswerSerializer(queryset, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def chapteranswerDetailByChapterid(request, pk):
    try:
        queryset = Chapteranswer.objects.filter(chapterid=pk)
    except Chapteranswer.DoesNotExist:
        return Response(chapteranswer_notfound, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChapteranswerSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def chapteranswerCreate(request):
    serializer = ChapteranswerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def chapteranswerUpdate(request, pk):
    chapteranswer = Chapteranswer.objects.get(chapteranswerid=pk)
    serializer = ChapteranswerSerializer(instance=chapteranswer, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def chapteranswerDelete(request, pk):
    try:
        chapteranswer = Chapteranswer.objects.get(chapteranswerid=pk)
    except Chapteranswer.DoesNotExist:
        return Response(chapteranswer_notfound, status=status.HTTP_404_NOT_FOUND)
    
    chapteranswer.delete()
    return Response({"msg" : "ลบบทเรียนสำเร็จ"}, status=status.HTTP_200_OK)

##########################################################################################