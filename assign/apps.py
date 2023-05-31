from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time, timedelta
import subprocess

def task():
    # 이용기간이 만료된 사물함 배정정보와 신청정보 삭제
    command = "python manage.py delete_expired_data"
    subprocess.run(command, shell=True)
    pass

class AssignAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assign'

    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(task, 'interval', minutes=1)  # 주기 설정 (예: 30분)
        scheduler.start()