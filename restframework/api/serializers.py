from rest_framework import serializers
from .models import *

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"

class ExamanswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examanswers
        fields = "__all__"

class ExaminformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examinformation
        fields = "__all__"

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"

class SubchapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subchapter
        fields = "__all__"

class ChapteranswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapteranswer
        fields = "__all__"

class QuesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quesheet
        fields = "__all__"

class QueheaddetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queheaddetails
        fields = "__all__"

class QuetopicdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quetopicdetails
        fields = "__all__"

class QueinformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queinformation
        fields = "__all__"