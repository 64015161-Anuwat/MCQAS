from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        # fields = ('userid', 'email', 'fullname', 'password', 
        #           'googleid', 'job', 'department','faculty', 
        #           'workplace', 'tel', 'usageformat','imge_kyc_path', 
        #           'e_kyc', 'typesid_user')

class CheckscoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checkscore
        fields = "__all__"
        # fields = ('scoreid', 'userid_score', 'activatekey_score')

class ExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = "__all__"
        # fields = ('examid', 'subid_exam', 'nameexam', 'examno', 
        #           'numexam', 'setexam', 'imganswers_format_path', 'std_csv_path',)

class ExamanswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Examanswers
        fields = "__all__"
        # fields = ('examanswersid', 'examid_ans', 'setexamans', 'scoringcriteria', 
        #           'papeans_path',)

class ExaminformationSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Examinformation
            fields = "__all__"
            # fields = ('examinfoid', 'examid_info', 'stdid', 'subidstd', 
            #           'examseatnumber', 'setexaminfo', 'section', 'score',
            #          'correct', 'wrong', 'unresponsive', 'anschoicestd',
            #         'activatekey_exan', 'imgansstd_path',)

# class ErrorsanswersheetSerializer(serializers.ModelSerializer):
    
#         class Meta:
#             model = Errorsanswersheet
#             fields = "__all__"
#             # fields = ('erroranssheetid', 'errorexamid_info', 'errorstdid', 'errorsubidstd',
#             #           'errorexamseatnumber', 'errorsetexaminfo', 'errorsection', 'errortype',
#             #           'errorimgansstd_path',)

class LessonSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Lesson
            fields = "__all__"
            # fields = ('lessonid', 'userid_lesson', 'namelesson', 'infolesson',)

class LessonanswerSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Lessonanswer
            fields = "__all__"
            # fields = ('lessonandanswer', 'examanswersid_lesans', 'sublessonid_lesans', 'choicelesson',)

class QueheaddetailsSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Queheaddetails
            fields = "__all__"
            # fields = ('queheaddetailsid', 'quesheetid_head', 'quehead1', 'quehead2',
            #          'quehead3', 'quehead4', 'quehead5',)

class QuesheetSerializer(serializers.ModelSerializer):
        
            class Meta:
                model = Quesheet
                fields = "__all__"
                # fields = ('quesheetid', 'userid_que', 'quesheetname', 'quesheettopicname',
                #          'detailslineone', 'detailslinetwo', 'explanation', 'symbolposition', 
                #          'imglogoquesheet_path', imgquesheet_path', 'activatekey_que', 'datetimestart',
                #          'datetimeend', 'statusquesheet',)

class QuetopicdetailsSerializer(serializers.ModelSerializer):
        
            class Meta:
                model = Quetopicdetails
                fields = "__all__"
                # fields = ('quetopicdetailsid', 'quesheetid_topic', 'quetopicnum', 'quetopicdetails',
                #          'quetopicformat', 'quetopictype',)

class QueinformationSerializer(serializers.ModelSerializer):
        
            class Meta:
                model = Queinformation
                fields = "__all__"
                # fields = ('queinfoid', 'quesheetid_queinfo', 'ansquehead', 'ansquetopic',
                #          'imgansstd_path', 'status_queinfo',)

class RequestSerializer(serializers.ModelSerializer):
        
            class Meta:
                model = Request
                fields = "__all__"
                # fields = ('requestid', 'userid_request', 'imgrequest_path', 'status_request',)

class RoleSerializer(serializers.ModelSerializer):
        
            class Meta:
                model = Role
                fields = "__all__"
                # fields = ('typesid', 'typesname', 'limitsub', 'limitque')

class SublessonSerializer(serializers.ModelSerializer):
        
            class Meta:
                model = Sublesson
                fields = "__all__"
                # fields = ('sublessonid', 'lessonid_sublessonid', 'numlesson', 'namelesson',
                #           'infolesson',)

class SubjectSerializer(serializers.ModelSerializer):
        
            class Meta:
                model = Subject
                fields = "__all__"
                # fields = ('subid', 'userid_sub', 'subjectid', 'subname',
                #           'year', 'semester',)