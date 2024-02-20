# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Chapter(models.Model):
    chapterid = models.AutoField(db_column='ChapterID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    namechapter = models.TextField(db_column='NameChapter', blank=True, null=True)  # Field name made lowercase.
    infochapter = models.TextField(db_column='InfoChapter', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Chapter'


class Chapteranswer(models.Model):
    chapteranswerid = models.AutoField(db_column='ChapterAnswerID', primary_key=True)  # Field name made lowercase.
    examanswersid = models.ForeignKey('Examanswers', models.DO_NOTHING, db_column='ExamAnswersID', blank=True, null=True)  # Field name made lowercase.
    subchapterid = models.ForeignKey('Subchapter', models.DO_NOTHING, db_column='SubChapterID', blank=True, null=True)  # Field name made lowercase.
    answerchapter = models.TextField(db_column='AnswerChapter', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChapterAnswer'


class Exam(models.Model):
    examid = models.AutoField(db_column='ExamID', primary_key=True)  # Field name made lowercase.
    subid = models.ForeignKey('Subject', models.DO_NOTHING, db_column='SubID', blank=True, null=True)  # Field name made lowercase.
    examname = models.TextField(db_column='ExamName', blank=True, null=True)  # Field name made lowercase.
    examno = models.IntegerField(db_column='ExamNo', blank=True, null=True)  # Field name made lowercase.
    numberofexams = models.IntegerField(db_column='NumberofExams', blank=True, null=True)  # Field name made lowercase.
    numberofexamsets = models.IntegerField(db_column='NumberofExamSets', blank=True, null=True)  # Field name made lowercase.
    answersheetformat = models.TextField(db_column='AnswerSheetFormat', blank=True, null=True)  # Field name made lowercase.
    imganswersheetformat_path = models.TextField(db_column='ImgAnswerSheetformat_path', blank=True, null=True)  # Field name made lowercase.
    std_csv_path = models.TextField(db_column='Std_csv_path', blank=True, null=True)  # Field name made lowercase.
    result_csv_path = models.TextField(db_column='Result_csv_path', blank=True, null=True)  # Field name made lowercase.
    analysis_csv_path = models.TextField(db_column='Analysis_csv_path', blank=True, null=True)  # Field name made lowercase.
    sequencesteps = models.TextField(db_column='SequenceSteps', blank=True, null=True)  # Field name made lowercase.
    showscores = models.IntegerField(db_column='ShowScores', blank=True, null=True)  # Field name made lowercase.
    sendemail = models.IntegerField(db_column='SendEmail', blank=True, null=True)  # Field name made lowercase.
    statusexam = models.TextField(db_column='StatusExam', blank=True, null=True)  # Field name made lowercase.
    deletetimeexam = models.DateTimeField(db_column='DeleteTimeExam', blank=True, null=True)  # Field name made lowercase.
    createtimeexam = models.DateTimeField(db_column='CreateTimeExam', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Exam'


class Examanswers(models.Model):
    examanswersid = models.AutoField(db_column='ExamAnswersID', primary_key=True)  # Field name made lowercase.
    examid = models.ForeignKey(Exam, models.DO_NOTHING, db_column='ExamID', blank=True, null=True)  # Field name made lowercase.
    examnoanswers = models.CharField(db_column='ExamNoAnswers', max_length=2, blank=True, null=True)  # Field name made lowercase.
    scoringcriteria = models.TextField(db_column='ScoringCriteria', blank=True, null=True)  # Field name made lowercase.
    choiceanswers = models.TextField(db_column='ChoiceAnswers', blank=True, null=True)  # Field name made lowercase.
    papeans_path = models.TextField(db_column='PapeAns_path', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExamAnswers'


class Examinformation(models.Model):
    examinfoid = models.AutoField(db_column='ExamInfoID', primary_key=True)  # Field name made lowercase.
    examid = models.ForeignKey(Exam, models.DO_NOTHING, db_column='ExamID', blank=True, null=True)  # Field name made lowercase.
    stdid = models.CharField(db_column='StdID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stdemail = models.CharField(db_column='StdEmail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    subjectidstd = models.CharField(db_column='SubjectIDStd', max_length=20, blank=True, null=True)  # Field name made lowercase.
    examseatnumber = models.CharField(db_column='ExamSeatNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.
    setexaminfo = models.IntegerField(db_column='SetExamInfo', blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=20, blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    correct = models.IntegerField(db_column='Correct', blank=True, null=True)  # Field name made lowercase.
    wrong = models.IntegerField(db_column='Wrong', blank=True, null=True)  # Field name made lowercase.
    unresponsive = models.IntegerField(db_column='Unresponsive', blank=True, null=True)  # Field name made lowercase.
    itemanalysis = models.TextField(db_column='ItemAnalysis', blank=True, null=True)  # Field name made lowercase.
    anschoicestd = models.TextField(db_column='AnsChoiceStd', blank=True, null=True)  # Field name made lowercase.
    imgansstd_path = models.TextField(db_column='ImgAnsStd_path', blank=True, null=True)  # Field name made lowercase.
    errorstype = models.TextField(db_column='ErrorsType', blank=True, null=True)  # Field name made lowercase.
    createtimeexaminfo = models.DateTimeField(db_column='CreateTimeExaminfo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExamInformation'


class Queheaddetails(models.Model):
    queheaddetailsid = models.AutoField(db_column='QueHeadDetailsID', primary_key=True)  # Field name made lowercase.
    quesheetid = models.ForeignKey('Quesheet', models.DO_NOTHING, db_column='QueSheetID', blank=True, null=True)  # Field name made lowercase.
    quehead1 = models.TextField(db_column='QueHead1', blank=True, null=True)  # Field name made lowercase.
    quehead2 = models.TextField(db_column='QueHead2', blank=True, null=True)  # Field name made lowercase.
    quehead3 = models.TextField(db_column='QueHead3', blank=True, null=True)  # Field name made lowercase.
    quehead4 = models.TextField(db_column='QueHead4', blank=True, null=True)  # Field name made lowercase.
    quehead5 = models.TextField(db_column='QueHead5', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QueHeadDetails'


class Queinformation(models.Model):
    queinfoid = models.AutoField(db_column='QueInfoID', primary_key=True)  # Field name made lowercase.
    quesheetid = models.ForeignKey('Quesheet', models.DO_NOTHING, db_column='QueSheetID', blank=True, null=True)  # Field name made lowercase.
    ansquehead = models.TextField(db_column='AnsQueHead', blank=True, null=True)  # Field name made lowercase.
    ansquetopic = models.TextField(db_column='AnsQueTopic', blank=True, null=True)  # Field name made lowercase.
    ansother = models.TextField(db_column='AnsOther', blank=True, null=True)  # Field name made lowercase.
    additionalsuggestions = models.TextField(db_column='Additionalsuggestions', blank=True, null=True)  # Field name made lowercase.
    imgansstd_path = models.TextField(db_column='ImgAnsStd_path', blank=True, null=True)  # Field name made lowercase.
    status_queinfo = models.TextField(db_column='Status_QueInfo', blank=True, null=True)  # Field name made lowercase.
    errorstype = models.TextField(db_column='ErrorsType', blank=True, null=True)  # Field name made lowercase.
    createtimequesheetinfo = models.DateTimeField(db_column='CreateTimeQueSheetinfo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QueInformation'


class Quesheet(models.Model):
    quesheetid = models.AutoField(db_column='QueSheetID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    quesheetname = models.TextField(db_column='QueSheetName', blank=True, null=True)  # Field name made lowercase.
    quesheettopicname = models.TextField(db_column='QueSheetTopicName', blank=True, null=True)  # Field name made lowercase.
    detailslineone = models.TextField(db_column='DetailsLineOne', blank=True, null=True)  # Field name made lowercase.
    detailslinetwo = models.TextField(db_column='DetailsLineTwo', blank=True, null=True)  # Field name made lowercase.
    imgquesheet_path = models.TextField(db_column='ImgQueSheet_path', blank=True, null=True)  # Field name made lowercase.
    resultpart1_csv_path = models.TextField(db_column='ResultPart1_csv_path', blank=True, null=True)  # Field name made lowercase.
    resultpart2_csv_path = models.TextField(db_column='ResultPart2_csv_path', blank=True, null=True)  # Field name made lowercase.
    datetimestart = models.DateTimeField(db_column='DateTimeStart', blank=True, null=True)  # Field name made lowercase.
    datetimeend = models.DateTimeField(db_column='DateTimeEnd', blank=True, null=True)  # Field name made lowercase.
    sequencesteps = models.TextField(db_column='SequenceSteps', blank=True, null=True)  # Field name made lowercase.
    statusquesheet = models.TextField(db_column='StatusQueSheet', blank=True, null=True)  # Field name made lowercase.
    deletetimequesheet = models.DateTimeField(db_column='DeleteTimeQueSheet', blank=True, null=True)  # Field name made lowercase.
    createtimequesheet = models.DateTimeField(db_column='CreateTimeQueSheet', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QueSheet'


class Quetopicdetails(models.Model):
    quetopicdetailsid = models.AutoField(db_column='QueTopicDetailsID', primary_key=True)  # Field name made lowercase.
    quesheetid = models.ForeignKey(Quesheet, models.DO_NOTHING, db_column='QueSheetID', blank=True, null=True)  # Field name made lowercase.
    quetopicdetails = models.TextField(db_column='QueTopicDetails', blank=True, null=True)  # Field name made lowercase.
    quetopicformat = models.TextField(db_column='QueTopicFormat', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QueTopicDetails'


class Request(models.Model):
    requestid = models.AutoField(db_column='RequestID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    imgrequest_path = models.TextField(db_column='ImgRequest_path', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    status_request = models.TextField(db_column='Status_Request', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Request'


class Subchapter(models.Model):
    subchapterid = models.AutoField(db_column='SubChapterID', primary_key=True)  # Field name made lowercase.
    chapterid = models.ForeignKey(Chapter, models.DO_NOTHING, db_column='ChapterID', blank=True, null=True)  # Field name made lowercase.
    numsubchapter = models.TextField(db_column='NumSubChapter', blank=True, null=True)  # Field name made lowercase.
    namesubchapter = models.TextField(db_column='NameSubChapter', blank=True, null=True)  # Field name made lowercase.
    infosubchapter = models.TextField(db_column='InfoSubChapter', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubChapter'


class Subject(models.Model):
    subid = models.AutoField(db_column='SubID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.CharField(db_column='SubjectID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    subjectname = models.CharField(db_column='SubjectName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    year = models.CharField(db_column='Year', max_length=10, blank=True, null=True)  # Field name made lowercase.
    semester = models.CharField(db_column='Semester', max_length=10, blank=True, null=True)  # Field name made lowercase.
    statussubject = models.TextField(db_column='StatusSubject', blank=True, null=True)  # Field name made lowercase.
    deletetimesubject = models.DateTimeField(db_column='DeleteTimeSubject', blank=True, null=True)  # Field name made lowercase.
    createtimesubject = models.DateTimeField(db_column='CreateTimeSubject', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Subject'


class Type(models.Model):
    typesid = models.AutoField(db_column='TypesID', primary_key=True)  # Field name made lowercase.
    typesname = models.CharField(db_column='TypesName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    limitsubject = models.IntegerField(db_column='LimitSubject', blank=True, null=True)  # Field name made lowercase.
    limitexam = models.IntegerField(db_column='LimitExam', blank=True, null=True)  # Field name made lowercase.
    limitque = models.IntegerField(db_column='LimitQue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Type'


class User(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fullname = models.TextField(db_column='FullName', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    salt = models.CharField(db_column='Salt', max_length=64, blank=True, null=True)  # Field name made lowercase.
    googleid = models.TextField(db_column='GoogleId', blank=True, null=True)  # Field name made lowercase.
    job = models.TextField(db_column='Job', blank=True, null=True)  # Field name made lowercase.
    department = models.TextField(db_column='Department', blank=True, null=True)  # Field name made lowercase.
    faculty = models.TextField(db_column='Faculty', blank=True, null=True)  # Field name made lowercase.
    workplace = models.TextField(db_column='Workplace', blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usageformat = models.CharField(db_column='Usageformat', max_length=10, blank=True, null=True)  # Field name made lowercase.
    imge_kyc_path = models.TextField(db_column='ImgE_KYC_path', blank=True, null=True)  # Field name made lowercase.
    e_kyc = models.CharField(db_column='E_KYC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    typesid = models.ForeignKey(Type, models.DO_NOTHING, db_column='TypesID', blank=True, null=True)  # Field name made lowercase.
    createtimeuser = models.DateTimeField(db_column='CreateTimeUser', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'
