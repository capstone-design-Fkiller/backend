from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from major.models import Major

import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed for Users"

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        majors = Major.objects.all()
        fake = Faker('ko_KR')

        for i in range(10):
            id = int(str(random.randint(2016, 2023)) + str(random.randint(10000, 99999)))
            password = 'qwer1234!'
            name = fake.name()
            #major = majors[random.randint(0, len(majors)-1)]
            major = majors[26-1] # 한교과로 assign 테스트
            is_adminable = False # 관리자 안 되게 허용
            is_usermode = True
            user = User(id=id, name=name, major=major)
            User.objects.create_user(id=id, password=password, name=name, major=major, is_usermode=is_usermode, is_adminable=is_adminable)

        self.stdout.write(self.style.SUCCESS("10 Users Seeded!"))