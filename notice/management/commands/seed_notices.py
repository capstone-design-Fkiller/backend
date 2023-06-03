from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from major.models import Major
from notice.models import Notice
from user.models import User

class Command(BaseCommand):
    help = 'Seed Notice Data'

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        majors = Major.objects.filter(pk__lte=16)

        for major in majors :
            admin = User.objects.filter(major = major, is_adminable=True).first()
            seeder.add_entity(Notice, 1, {
                'major': major,
                'title' : "사물함 반납 안내",
                'content' : "2월 30까지 사물함을 모두 비워주시기 바랍니다",
                'writer': admin
            })

        for major in majors :
            admin = User.objects.filter(major = major, is_adminable=True).first()
            seeder.add_entity(Notice, 1, {
                'major': major,
                'title' : "사물함신청 공지",
                'content' : "사물함 신청기간 : 6월 1일 ~ 6월 20일\n사물함 이용기간 : 7월1일 ~ 8월1일\n사물함 배정기준은 학생회비 납부여부, 통학시간입니다",
                'writer': admin
            })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Notice data, Success!"))