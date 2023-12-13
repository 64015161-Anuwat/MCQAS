# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Checkscore(models.Model):
    scoreid = models.AutoField(db_column='ScoreID', primary_key=True)  # Field name made lowercase.
    userid_score = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID_Score', blank=True, null=True)  # Field name made lowercase.
    activatekey_score = models.TextField(db_column='ActivateKey_Score', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CheckScore'


class Errorsanswersheet(models.Model):
    errorsanssheetid = models.AutoField(db_column='ErrorsAnsSheetID', primary_key=True)  # Field name made lowercase.
    errorexamid_info = models.ForeignKey('Exam', models.DO_NOTHING, db_column='ErrorExamID_info', blank=True, null=True)  # Field name made lowercase.
    errorstdid = models.CharField(db_column='ErrorStdID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    errorsubidstd = models.CharField(db_column='ErrorSubIDStd', max_length=20, blank=True, null=True)  # Field name made lowercase.
    errorexamseatnumber = models.CharField(db_column='ErrorExamSeatNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.
    errorsetexaminfo = models.IntegerField(db_column='ErrorSetExamInfo', blank=True, null=True)  # Field name made lowercase.
    errorsection = models.CharField(db_column='ErrorSection', max_length=20, blank=True, null=True)  # Field name made lowercase.
    errorstype = models.TextField(db_column='ErrorsType', blank=True, null=True)  # Field name made lowercase.
    errorimgansstd_path = models.TextField(db_column='ErrorImgAnsStd_path', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ErrorsAnswerSheet'


class Exam(models.Model):
    examid = models.AutoField(db_column='ExamID', primary_key=True)  # Field name made lowercase.
    subid_exam = models.ForeignKey('Subject', models.DO_NOTHING, db_column='SubID_exam', blank=True, null=True)  # Field name made lowercase.
    nameexam = models.TextField(db_column='NameExam', blank=True, null=True)  # Field name made lowercase.
    examno = models.IntegerField(db_column='ExamNo', blank=True, null=True)  # Field name made lowercase.
    numexam = models.IntegerField(db_column='NumExam', blank=True, null=True)  # Field name made lowercase.
    setexam = models.IntegerField(db_column='SetExam', blank=True, null=True)  # Field name made lowercase.
    imganswers_format_path = models.TextField(db_column='ImgAnswerS_format_path', blank=True, null=True)  # Field name made lowercase.
    std_csv_path = models.TextField(db_column='Std_csv_path', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Exam'


class Examanswers(models.Model):
    examanswersid = models.AutoField(db_column='ExamAnswersID', primary_key=True)  # Field name made lowercase.
    examid_ans = models.ForeignKey(Exam, models.DO_NOTHING, db_column='ExamID_Ans', blank=True, null=True)  # Field name made lowercase.
    setexamans = models.CharField(db_column='SetExamAns', max_length=2, blank=True, null=True)  # Field name made lowercase.
    scoringcriteria = models.TextField(db_column='ScoringCriteria', blank=True, null=True)  # Field name made lowercase.
    papeans_path = models.TextField(db_column='PapeAns_path', blank=True, null=True)  # Field name made lowercase.
    answers = models.TextField(db_column='Answers', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExamAnswers'


class Examinformation(models.Model):
    examinfoid = models.AutoField(db_column='ExaminfoID', primary_key=True)  # Field name made lowercase.
    examid_info = models.ForeignKey(Exam, models.DO_NOTHING, db_column='ExamID_info', blank=True, null=True)  # Field name made lowercase.
    stdid = models.CharField(db_column='StdID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    subidstd = models.CharField(db_column='SubIDStd', max_length=20, blank=True, null=True)  # Field name made lowercase.
    examseatnumber = models.CharField(db_column='ExamSeatNumber', max_length=20, blank=True, null=True)  # Field name made lowercase.
    setexaminfo = models.CharField(db_column='SetExamInfo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=20, blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    correct = models.IntegerField(db_column='Correct', blank=True, null=True)  # Field name made lowercase.
    wrong = models.IntegerField(db_column='Wrong', blank=True, null=True)  # Field name made lowercase.
    unresponsive = models.IntegerField(db_column='Unresponsive', blank=True, null=True)  # Field name made lowercase.
    anschoicestd = models.TextField(db_column='AnsChoiceStd', blank=True, null=True)  # Field name made lowercase.
    activatekey_exan = models.CharField(db_column='ActivateKey_Exan', max_length=100, blank=True, null=True)  # Field name made lowercase.
    imgansstd_path = models.TextField(db_column='ImgAnsStd_path', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Examinformation'


class Lesson(models.Model):
    lessonid = models.AutoField(db_column='LessonID', primary_key=True)  # Field name made lowercase.
    userid_lesson = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID_Lesson', blank=True, null=True)  # Field name made lowercase.
    namelesson = models.TextField(db_column='NameLesson', blank=True, null=True)  # Field name made lowercase.
    infolesson = models.TextField(db_column='InfoLesson', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Lesson'


class Lessonanswer(models.Model):
    lessonandanswer = models.AutoField(db_column='LessonAndAnswer', primary_key=True)  # Field name made lowercase.
    examanswersid_lesans = models.ForeignKey(Examanswers, models.DO_NOTHING, db_column='ExamAnswersID_LesAns', blank=True, null=True)  # Field name made lowercase.
    sublessonid_lesans = models.ForeignKey('Sublesson', models.DO_NOTHING, db_column='SubLessonID_LesAns', blank=True, null=True)  # Field name made lowercase.
    choicelesson = models.TextField(db_column='ChoiceLesson', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LessonAnswer'


class Queheaddetails(models.Model):
    queheaddetailsid = models.AutoField(db_column='QueHeadDetailsID', primary_key=True)  # Field name made lowercase.
    quesheetid_head = models.ForeignKey('Quesheet', models.DO_NOTHING, db_column='QueSheetID_Head', blank=True, null=True)  # Field name made lowercase.
    quehead1 = models.TextField(db_column='QueHead1', blank=True, null=True)  # Field name made lowercase.
    quehead2 = models.TextField(db_column='QueHead2', blank=True, null=True)  # Field name made lowercase.
    quehead3 = models.TextField(db_column='QueHead3', blank=True, null=True)  # Field name made lowercase.
    quehead4 = models.TextField(db_column='QueHead4', blank=True, null=True)  # Field name made lowercase.
    quehead5 = models.TextField(db_column='QueHead5', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QueHeadDetails'


class Quesheet(models.Model):
    quesheetid = models.AutoField(db_column='QueSheetID', primary_key=True)  # Field name made lowercase.
    userid_que = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID_Que', blank=True, null=True)  # Field name made lowercase.
    quesheetname = models.TextField(db_column='QueSheetName', blank=True, null=True)  # Field name made lowercase.
    quesheettopicname = models.TextField(db_column='QueSheetTopicName', blank=True, null=True)  # Field name made lowercase.
    detailslineone = models.TextField(db_column='DetailsLineOne', blank=True, null=True)  # Field name made lowercase.
    detailslinetwo = models.TextField(db_column='DetailsLinetwo', blank=True, null=True)  # Field name made lowercase.
    explanation = models.TextField(db_column='Explanation', blank=True, null=True)  # Field name made lowercase.
    symbolposition = models.CharField(db_column='Symbolposition', max_length=10, blank=True, null=True)  # Field name made lowercase.
    imglogoquesheet_path = models.TextField(db_column='ImgLogoQueSheet_path', blank=True, null=True)  # Field name made lowercase.
    imgquesheet_path = models.TextField(db_column='ImgQueSheet_path', blank=True, null=True)  # Field name made lowercase.
    activatekey_que = models.TextField(db_column='ActivateKey_Que', blank=True, null=True)  # Field name made lowercase.
    datetimestart = models.DateTimeField(db_column='DateTimeStart', blank=True, null=True)  # Field name made lowercase.
    datetimeend = models.DateTimeField(db_column='DateTimeEnd', blank=True, null=True)  # Field name made lowercase.
    statusquesheet = models.CharField(db_column='StatusQueSheet', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QueSheet'


class Quetopicdetails(models.Model):
    quetopicdetailsid = models.AutoField(db_column='QueTopicDetailsID', primary_key=True)  # Field name made lowercase.
    quesheetid_topic = models.ForeignKey(Quesheet, models.DO_NOTHING, db_column='QueSheetID_Topic', blank=True, null=True)  # Field name made lowercase.
    quetopicnum = models.TextField(db_column='QueTopicNum', blank=True, null=True)  # Field name made lowercase.
    quetopicdetails = models.TextField(db_column='QueTopicDetails', blank=True, null=True)  # Field name made lowercase.
    quetopicformat = models.TextField(db_column='QueTopicFormat', blank=True, null=True)  # Field name made lowercase.
    quetopictype = models.TextField(db_column='QueTopicType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QueTopicDetails'


class Queinformation(models.Model):
    queinfoid = models.AutoField(db_column='QueinfoID', primary_key=True)  # Field name made lowercase.
    quesheetid_queinfo = models.ForeignKey(Quesheet, models.DO_NOTHING, db_column='QueSheetID_QueInfo', blank=True, null=True)  # Field name made lowercase.
    ansquehead = models.TextField(db_column='AnsQueHead', blank=True, null=True)  # Field name made lowercase.
    ansquetopic = models.TextField(db_column='AnsQueTopic', blank=True, null=True)  # Field name made lowercase.
    imgansstd_path = models.TextField(db_column='ImgAnsStd_path', blank=True, null=True)  # Field name made lowercase.
    status_queinfo = models.CharField(db_column='Status_QueInfo', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Queinformation'


class Request(models.Model):
    requestid = models.AutoField(db_column='RequestID', primary_key=True)  # Field name made lowercase.
    userid_request = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID_Request', blank=True, null=True)  # Field name made lowercase.
    imgrequest_path = models.TextField(db_column='ImgRequest_path', blank=True, null=True)  # Field name made lowercase.
    status_request = models.IntegerField(db_column='Status_Request', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Request'


class Role(models.Model):
    typesid = models.AutoField(db_column='TypesID', primary_key=True)  # Field name made lowercase.
    typesname = models.CharField(db_column='TypesName', max_length=40, blank=True, null=True)  # Field name made lowercase.
    limitsub = models.IntegerField(db_column='LimitSub', blank=True, null=True)  # Field name made lowercase.
    limitque = models.IntegerField(db_column='LimitQue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Role'


class Sublesson(models.Model):
    sublessonid = models.AutoField(db_column='SubLessonID', primary_key=True)  # Field name made lowercase.
    lessonid_sublessonid = models.ForeignKey(Lesson, models.DO_NOTHING, db_column='LessonID_SubLessonID', blank=True, null=True)  # Field name made lowercase.
    numlesson = models.TextField(db_column='NumLesson', blank=True, null=True)  # Field name made lowercase.
    namelesson = models.TextField(db_column='NameLesson', blank=True, null=True)  # Field name made lowercase.
    infolesson = models.TextField(db_column='InfoLesson', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubLesson'


class Subject(models.Model):
    subid = models.AutoField(db_column='SubID', primary_key=True)  # Field name made lowercase.
    userid_sub = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID_Sub', blank=True, null=True)  # Field name made lowercase.
    subjectid = models.CharField(db_column='SubjectID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    subname = models.CharField(db_column='SubName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    year = models.CharField(db_column='Year', max_length=10, blank=True, null=True)  # Field name made lowercase.
    semester = models.CharField(db_column='Semester', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Subject'


class User(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fullname = models.TextField(db_column='FullName', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=60, blank=True, null=True)  # Field name made lowercase.
    googleid = models.TextField(db_column='googleId', blank=True, null=True)  # Field name made lowercase.
    job = models.TextField(db_column='Job', blank=True, null=True)  # Field name made lowercase.
    department = models.TextField(db_column='Department', blank=True, null=True)  # Field name made lowercase.
    faculty = models.TextField(db_column='Faculty', blank=True, null=True)  # Field name made lowercase.
    workplace = models.TextField(db_column='Workplace', blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usageformat = models.CharField(db_column='Usageformat', max_length=10, blank=True, null=True)  # Field name made lowercase.
    imge_kyc_path = models.TextField(db_column='ImgE_KYC_path', blank=True, null=True)  # Field name made lowercase.
    e_kyc = models.CharField(db_column='E_KYC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    typesid_user = models.ForeignKey(Role, models.DO_NOTHING, db_column='TypesID_User', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
