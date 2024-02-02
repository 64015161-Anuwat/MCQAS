from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # fields = ('userid', 'email', 'fullname', 'password',
        #           'salt', 'googleid', 'job',
        #           'department','faculty', 'workplace', 
        #           'tel', 'usageformat','imge_kyc_path', 'e_kyc',
        #           'typesid_user', 'createtime_user')

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"
        # fields = ('typesid', 'typesname', 'limitsubject', 'limitexam', 'limitque')

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
        # fields = ('requestid', 'userid', 'imgrequest_path', 'notes', 'status_request',)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
        # fields = ('subid', 'userid', 'subjectid', 'subjectname',
        #           'year', 'semester', 'statussubject', 'deletetime_subject',
        #           'createtime_subject')

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"
        # fields = ('examid', 'subid', 'nameexam', 'examno', 
        #           'numberofexams', 'numberofexamsets', 'answersheetformat', 'imganswersheetformat_path',
        #           'std_csv_path', 'sequencesteps', 'showscores', 'sendmail',
        #           'statusexam', 'createtime_exam', 'deletetime_exam')

class ExamanswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examanswers
        fields = "__all__"
        # fields = ('examanswersid', 'examid', 'examnoanswers', 'scoringcriteria', 
        #           'choiceanswers', 'papeans_path',)

class ExaminformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examinformation
        fields = "__all__"
        # fields = ('examinfoid', 'examid', 'stdid', 'stdemail',
        #           'subjectidstd', 'examseatnumber', 'setexaminfo', 'section',
        #           'score', 'correct', 'wrong', 'unresponsive',
        #           'itemanalysis', 'anschoicestd', 'imgansstd_path', 'errortype'
        #           'createtime_std')

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"
        # fields = ('chapterid', 'userid', 'namechapter', 'infochapter',)

class SubchapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subchapter
        fields = "__all__"
        # fields = ('subchapterid', 'chapterid', 'numsubchapter', 'namesubchapter',
        #           'infosubchapter',)

class ChapteranswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapteranswer
        fields = "__all__"
        # fields = ('chapteranswerid', 'examanswersid', 'subchapterid', 'answerchapter',)

class QuesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quesheet
        fields = "__all__"
        # fields = ('quesheetid', 'userid', 'quesheetname', 'quesheettopicname',
        #           'detailslineone', 'detailslinetwo', 'explanation', 'imgquesheet_path', 
        #           'datetimestart', 'datetimeend', 'statusquesheet', 'deletetime_quesheet', 
        #           'createtime_quesheet',)

class QueheaddetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queheaddetails
        fields = "__all__"
        # fields = ('queheaddetailsid', 'quesheetid', 'quehead1', 'quehead2',
        #           'quehead3', 'quehead4', 'quehead5',)

class QuetopicdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quetopicdetails
        fields = "__all__"
        # fields = ('quetopicdetailsid', 'quesheetid', 'quetopicnum', 'quetopicdetails',
        #           'quetopicformat')

class QueinformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queinformation
        fields = "__all__"
        # fields = ('queinfoid', 'quesheetid', 'ansquehead', 'ansquetopic',
        #           'imgansstd_path', 'status_queinfo', 'errortype', 'createtime_queinfo')