# tasks.py
from celery import shared_task
from .models import *
from datetime import datetime
from django.utils import timezone

@shared_task
def update_data_task():
    # current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00")
    current_time = timezone.now()
    subject = Subject.objects.filter(deletetimesubject__lt=current_time)
    for sub in subject:
        sub.statussubject = '0'
        sub.save()
    exam = Exam.objects.filter(deletetimeexam__lt=current_time)
    for ex in exam:
        ex.statusexam = '0'
        ex.save()
    quesheet = Quesheet.objects.filter(deletetimequesheet__lt=current_time)
    for qtn in quesheet:
        qtn.statusquesheet = '0'
        qtn.save()
