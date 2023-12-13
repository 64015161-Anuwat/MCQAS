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
    path('user/update/<str:pk>/', views.userUpdate, name='User-Update'),
    path('user/delete/<str:pk>/', views.userDelete, name='User-Delete'),
    path('user/duplicate/email/', views.userDuplicateEmail, name='User-Duplicate-Email'),
    path('user/duplicate/googleid/', views.userDuplicateGoogleid, name='User-Duplicate-Googleid'),
    path('user/login/', views.userLogin, name='User-Login'),
    path('user/login/google/', views.userLoginGoogle, name='User-Login-Google'),
    ############################################################
    path('checkscore/', views.checkscoreList, name='Checkscore-List'),
    path('checkscore/detail/<str:pk>/', views.checkscoreDetail, name='Checkscore-Detail'),
    path('checkscore/create/', views.checkscoreCreate, name='Checkscore-Create'),
    path('checkscore/update/<str:pk>/', views.checkscoreUpdate, name='Checkscore-Update'),
    path('checkscore/delete/<str:pk>/', views.checkscoreDelete, name='Checkscore-Delete'),
    ############################################################
    path('exam/', views.examList, name='Exam-List'),
    path('exam/detail/<str:pk>/', views.examDetail, name='Exam-Detail'),
    path('exam/create/', views.examCreate, name='Exam-Create'),
    path('exam/update/<str:pk>/', views.examUpdate, name='Exam-Update'),
    path('exam/delete/<str:pk>/', views.examDelete, name='Exam-Delete'),
    path('exam/upload/csv/', views.examUploadCSV, name='Exam-Upload-CSV'),
    path('exam/upload/logo/', views.examUploadLogo, name='Exam-Upload-Logo'),
    ############################################################
    path('examanswers/', views.examanswersList, name='Examanswers-List'),
    path('examanswers/detail/<str:pk>/', views.examanswersDetail, name='Examanswers-Detail'),
    path('examanswers/create/', views.examanswersCreate, name='Examanswers-Create'),
    path('examanswers/update/<str:pk>/', views.examanswersUpdate, name='Examanswers-Update'),
    path('examanswers/delete/<str:pk>/', views.examanswersDelete, name='Examanswers-Delete'),
    path('examanswers/upload/paperans/', views.examanswersUploadPaperans, name='Examanswers-Upload-Paperans'), 
    ############################################################
    path('examinformation/', views.examinformationList, name='Examinformation-List'),
    path('examinformation/detail/<str:pk>/', views.examinformationDetail, name='Examinformation-Detail'),
    path('examinformation/create/', views.examinformationCreate, name='Examinformation-Create'),
    path('examinformation/update/<str:pk>/', views.examinformationUpdate, name='Examinformation-Update'),
    path('examinformation/delete/<str:pk>/', views.examinformationDelete, name='Examinformation-Delete'),
    path('examinformation/upload/paperans/', views.examinformationUploadPaperans, name='Examinformation-Upload-Paper'),
    ############################################################
    path('errorsanswersheet/', views.errorsanswersheetList, name='Erroranswersheet-List'),
    path('errorsanswersheet/detail/<str:pk>/', views.errorsanswersheetDetail, name='Erroranswersheet-Detail'),
    path('errorsanswersheet/create/', views.errorsanswersheetCreate, name='Erroranswersheet-Create'),
    path('errorsanswersheet/update/<str:pk>/', views.errorsanswersheetUpdate, name='Erroranswersheet-Update'),
    path('errorsanswersheet/delete/<str:pk>/', views.errorsanswersheetDelete, name='Erroranswersheet-Delete'),
    ############################################################
    path('lesson/', views.lessonList, name='Lesson-List'),
    path('lesson/detail/<str:pk>/', views.lessonDetail, name='Lesson-Detail'),
    path('lesson/create/', views.lessonCreate, name='Lesson-Create'),
    path('lesson/update/<str:pk>/', views.lessonUpdate, name='Lesson-Update'),
    path('lesson/delete/<str:pk>/', views.lessonDelete, name='Lesson-Delete'),
    ############################################################
    path('lessonanswer/', views.lessonanswerList, name='Lessonanswer-List'),
    path('lessonanswer/detail/<str:pk>/', views.lessonanswerDetail, name='Lessonanswer-Detail'),
    path('lessonanswer/create/', views.lessonanswerCreate, name='Lessonanswer-Create'),
    path('lessonanswer/update/<str:pk>/', views.lessonanswerUpdate, name='Lessonanswer-Update'),
    path('lessonanswer/delete/<str:pk>/', views.lessonanswerDelete, name='Lessonanswer-Delete'),
    ############################################################
    path('queheaddetails/', views.queheaddetailsList, name='Queheaddetails-List'),
    path('queheaddetails/detail/<str:pk>/', views.queheaddetailsDetail, name='Queheaddetails-Detail'),
    path('queheaddetails/create/', views.queheaddetailsCreate, name='Queheaddetails-Create'),
    path('queheaddetails/update/<str:pk>/', views.queheaddetailsUpdate, name='Queheaddetails-Update'),
    path('queheaddetails/delete/<str:pk>/', views.queheaddetailsDelete, name='Queheaddetails-Delete'),
    ############################################################
    path('quesheet/', views.quesheetList, name='Quesheet-List'),
    path('quesheet/detail/<str:pk>/', views.quesheetDetail, name='Quesheet-Detail'),
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
    path('queinformation/create/', views.queinformationCreate, name='Queinformation-Create'),
    path('queinformation/update/<str:pk>/', views.queinformationUpdate, name='Queinformation-Update'),
    path('queinformation/delete/<str:pk>/', views.queinformationDelete, name='Queinformation-Delete'),
    ############################################################
    path('request/', views.requestList, name='Request-List'),
    path('request/detail/<str:pk>/', views.requestDetail, name='Request-Detail'),
    path('request/create/', views.requestCreate, name='Request-Create'),
    path('request/update/<str:pk>/', views.requestUpdate, name='Request-Update'),
    path('request/delete/<str:pk>/', views.requestDelete, name='Request-Delete'),
    ############################################################
    path('role/', views.roleList, name='Role-List'),
    path('role/detail/<str:pk>/', views.roleDetail, name='Role-Detail'),
    path('role/create/', views.roleCreate, name='Role-Create'),
    path('role/update/<str:pk>/', views.roleUpdate, name='Role-Update'),
    path('role/delete/<str:pk>/', views.roleDelete, name='Role-Delete'),
    ############################################################
    path('sublesson/', views.sublessonList, name='Sublesson-List'),
    path('sublesson/detail/<str:pk>/', views.sublessonDetail, name='Sublesson-Detail'),
    path('sublesson/create/', views.sublessonCreate, name='Sublesson-Create'),
    path('sublesson/update/<str:pk>/', views.sublessonUpdate, name='Sublesson-Update'),
    path('sublesson/delete/<str:pk>/', views.sublessonDelete, name='Sublesson-Delete'),
    ############################################################
    path('subject/', views.subjectList, name='Subject-List'),
    path('subject/detail/<str:pk>/', views.subjectDetail, name='Subject-Detail'),
    path('subject/create/', views.subjectCreate, name='Subject-Create'),
    path('subject/update/<str:pk>/', views.subjectUpdate, name='Subject-Update'),
    path('subject/delete/<str:pk>/', views.subjectDelete, name='Subject-Delete'),
    ############################################################

]