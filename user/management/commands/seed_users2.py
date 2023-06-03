from django_seed import Seed
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from major.models import Major
import info

import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed for Users"

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        majors = Major.objects.all()
        fake = Faker('ko_KR')

        USER_COUNT = 30

        user_test_majors = Major.objects.filter(pk__lte=16)
        admin_test_majors = Major.objects.filter(pk__gte=17)

        for major in user_test_majors :
            print(major)
            id = int(str(random.randint(2016, 2023)) + str(random.randint(10000, 99999)))
            password = 'qwer1234!'
            name = fake.name()
            major = major
            is_adminable = True
            is_usermode = True
            User.objects.create_user(id=id, password=password, name=name, major=major, is_usermode=is_usermode, is_adminable=is_adminable)

        for i in range(USER_COUNT):            
            for major in admin_test_majors :
                print(major)
                id = int(str(random.randint(2016, 2023)) + str(random.randint(10000, 99999)))
                password = 'qwer1234!'
                name = fake.name()
                major = major # 한교과로 assign 테스트
                is_adminable = False # 관리자 안 되게 허용
                if i < 10 :
                    is_adminable = True # 관리자 되게 허용
                is_usermode = True
                User.objects.create_user(id=id, password=password, name=name, major=major, is_usermode=is_usermode, is_adminable=is_adminable)

        self.stdout.write(self.style.SUCCESS(f"Users Seeded!"))