"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.overview, name='API-Overview'),
    path('user/', views.userList, name='User-List'),
    path('user/detail/<str:pk>/', views.userDetail, name='User-Detail'),
    path('user/create/', views.userCreate, name='User-Create'),
    path('verify/email/<str:e_kyc>/', views.userVerifyEmail, name='User-Verify-Email'),
    path('user/update/<str:pk>/', views.userUpdate, name='User-Update'),
    path('user/delete/<str:pk>/', views.userDelete, name='User-Delete'),
    path('user/duplicate/email/<str:email>/', views.userDuplicateEmail, name='User-Duplicate-Email'),
    path('user/duplicate/googleid/<str:googleid>/', views.userDuplicateGoogleid, name='User-Duplicate-Googleid'),
    path('user/login/', views.userLogin, name='User-Login'),
    path('user/login/google/', views.userLoginGoogle, name='User-Login-Google'),
    ############################################################
    path('exam/', views.examList, name='Exam-List'),
    path('exam/detail/<str:pk>/', views.examDetail, name='Exam-Detail'),
    path('exam/detail/subject/<str:pk>/', views.examDetailBySubid, name='Exam-Detail-Subject'),
    path('exam/create/', views.examCreate, name='Exam-Create'),
    path('exam/update/<str:pk>/', views.examUpdate, name='Exam-Update'),
    path('exam/delete/<str:pk>/', views.examDelete, name='Exam-Delete'),
    path('exam/upload/csv/', views.examUploadCSV, name='Exam-Upload-CSV'),
    path('exam/upload/logo/', views.examUploadLogo, name='Exam-Upload-Logo'),
    path('exam/sendmail/<str:pk>/', views.examSendMail, name='Exam-Send-Mail'),
    ############################################################
    path('examanswers/', views.examanswersList, name='Examanswers-List'),
    path('examanswers/detail/<str:pk>/', views.examanswersDetail, name='Examanswers-Detail'),
    path('examanswers/detail/exam/<str:pk>/', views.examanswersDetailByExamid, name='Examanswers-Detail-Exam'),
    path('examanswers/create/', views.examanswersCreate, name='Examanswers-Create'),
    path('examanswers/update/<str:pk>/', views.examanswersUpdate, name='Examanswers-Update'),
    path('examanswers/delete/<str:pk>/', views.examanswersDelete, name='Examanswers-Delete'),
    path('examanswers/upload/paper/', views.examanswersUploadPaper, name='Examanswers-Upload-Paper'), 
    ############################################################
    path('examinformation/', views.examinformationList, name='Examinformation-List'),
    path('examinformation/detail/<str:pk>/', views.examinformationDetail, name='Examinformation-Detail'),
    path('examinformation/detail/exam/<str:pk>/', views.examinformationDetailByExamid, name='Examinformation-Detail-Exam'),
    path('examinformation/detail/email/<str:pk>/', views.examinformationDetailByEmail, name='Examinformation-Detail-Email'),
    path('examinformation/create/', views.examinformationCreate, name='Examinformation-Create'),
    path('examinformation/update/<str:pk>/', views.examinformationUpdate, name='Examinformation-Update'),
    path('examinformation/delete/<str:pk>/', views.examinformationDelete, name='Examinformation-Delete'),
    path('examinformation/upload/paper/', views.examinformationUploadPaper, name='Examinformation-Upload-Paper'),
    path('examinformation/tableans/<str:pk>/', views.examinformationTableAns, name='Examinformation-TableAns'),
    path('examinformation/result/<str:pk>/', views.examinformationResult, name='Examinformation-Result'),
    ############################################################
    path('chapter/', views.chapterList, name='chapter-List'),
    path('chapter/detail/<str:pk>/', views.chapterDetail, name='chapter-Detail'),
    path('chapter/detail/user/<str:pk>/', views.chapterDetailByUserid, name='chapter-Detail-User'),
    path('chapter/create/', views.chapterCreate, name='chapter-Create'),
    path('chapter/update/<str:pk>/', views.chapterUpdate, name='chapter-Update'),
    path('chapter/delete/<str:pk>/', views.chapterDelete, name='chapter-Delete'),
    ############################################################
    path('chapteranswer/', views.chapteranswerList, name='chapteranswer-List'),
    path('chapteranswer/detail/<str:pk>/', views.chapteranswerDetail, name='chapteranswer-Detail'),
    path('chapteranswer/detail/chapter/<str:pk>/', views.chapteranswerDetailByChapterid, name='chapteranswer-Detail-Chapter'),
    path('chapteranswer/create/', views.chapteranswerCreate, name='chapteranswer-Create'),
    path('chapteranswer/update/<str:pk>/', views.chapteranswerUpdate, name='chapteranswer-Update'),
    path('chapteranswer/delete/<str:pk>/', views.chapteranswerDelete, name='chapteranswer-Delete'),
    ############################################################
    path('queheaddetails/', views.queheaddetailsList, name='Queheaddetails-List'),
    path('queheaddetails/detail/<str:pk>/', views.queheaddetailsDetail, name='Queheaddetails-Detail'),
    path('queheaddetails/create/', views.queheaddetailsCreate, name='Queheaddetails-Create'),
    path('queheaddetails/update/<str:pk>/', views.queheaddetailsUpdate, name='Queheaddetails-Update'),
    path('queheaddetails/delete/<str:pk>/', views.queheaddetailsDelete, name='Queheaddetails-Delete'),
    ############################################################
    path('quesheet/', views.quesheetList, name='Quesheet-List'),
    path('quesheet/detail/<str:pk>/', views.quesheetDetail, name='Quesheet-Detail'),
    path('quesheet/detail/user/<str:pk>/', views.quesheetDetailByUserid, name='Quesheet-Detail-User'),
    path('quesheet/create/', views.quesheetCreate, name='Quesheet-Create'),
    path('quesheet/update/<str:pk>/', views.quesheetUpdate, name='Quesheet-Update'),
    path('quesheet/delete/<str:pk>/', views.quesheetDelete, name='Quesheet-Delete'),
    ############################################################
    path('quetopicdetails/', views.quetopicdetailsList, name='Quetopicdetails-List'),
    path('quetopicdetails/detail/<str:pk>/', views.quetopicdetailsDetail, name='Quetopicdetails-Detail'),
    path('quetopicdetails/create/', views.quetopicdetailsCreate, name='Quetopicdetails-Create'),
    path('quetopicdetails/update/<str:pk>/', views.quetopicdetailsUpdate, name='Quetopicdetails-Update'),
    path('quetopicdetails/delete/<str:pk>/', views.quetopicdetailsDelete, name='Quetopicdetails-Delete'),
    ############################################################
    path('queinformation/', views.queinformationList, name='Queinformation-List'),
    path('queinformation/detail/<str:pk>/', views.queinformationDetail, name='Queinformation-Detail'),
    path('queinformation/detail/quesheet/<str:pk>/', views.queinformationDetailByQuesheetid, name='Queinformation-Detail-By-Quesheet'),
    path('queinformation/create/', views.queinformationCreate, name='Queinformation-Create'),
    path('queinformation/update/<str:pk>/', views.queinformationUpdate, name='Queinformation-Update'),
    path('queinformation/delete/<str:pk>/', views.queinformationDelete, name='Queinformation-Delete'),
    path('queinformation/upload/paper/', views.queinformationUploadPaper, name='Queinformation-Upload-Paper'),
    path('queinformation/result/<str:pk>/', views.queinformationResult, name='Queinformation-Result'),
    ############################################################
    path('request/', views.requestList, name='Request-List'),
    path('request/detail/<str:pk>/', views.requestDetail, name='Request-Detail'),
    path('request/detail/user/<str:pk>/', views.requestDetailByUserid, name='Request-Detail-User'),
    path('request/create/', views.requestCreate, name='Request-Create'),
    path('request/update/<str:pk>/', views.requestUpdate, name='Request-Update'),
    path('request/delete/<str:pk>/', views.requestDelete, name='Request-Delete'),
    ############################################################
    path('type/', views.typeList, name='type-List'),
    path('type/detail/<str:pk>/', views.typeDetail, name='type-Detail'),
    path('type/create/', views.typeCreate, name='type-Create'),
    path('type/update/<str:pk>/', views.typeUpdate, name='type-Update'),
    path('type/delete/<str:pk>/', views.typeDelete, name='type-Delete'),
    ############################################################
    path('subchapter/', views.subchapterList, name='subchapter-List'),
    path('subchapter/detail/<str:pk>/', views.subchapterDetail, name='subchapter-Detail'),
    path('subchapter/detail/chapter/<str:pk>/', views.subchapterDetailByChapterid, name='subchapter-Detail-Chapter'),
    path('subchapter/create/', views.subchapterCreate, name='subchapter-Create'),
    path('subchapter/update/<str:pk>/', views.subchapterUpdate, name='subchapter-Update'),
    path('subchapter/delete/<str:pk>/', views.subchapterDelete, name='subchapter-Delete'),
    ############################################################
    path('subject/', views.subjectList, name='Subject-List'),
    path('subject/detail/<str:pk>/', views.subjectDetail, name='Subject-Detail'),
    path('subject/detail/user/<str:pk>/', views.subjectDetailByUserid, name='Subject-Detail-User'),
    path('subject/create/', views.subjectCreate, name='Subject-Create'),
    path('subject/update/<str:pk>/', views.subjectUpdate, name='Subject-Update'),
    path('subject/delete/<str:pk>/', views.subjectDelete, name='Subject-Delete'),
    ############################################################
    path('update/', views.update, name='Update'),
    ############################################################
]