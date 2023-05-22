from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from apply.models import Apply
from user.models import User
from major.models import Major
from locker.models import Building
from faker import Faker
import random



class Command(BaseCommand):
    help = 'Seed Major data'

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        fake = Faker()

        seeder.add_entity(Apply, 50, {
            'major': lambda x: Major.objects.filter(id__in=[26]).order_by('?').first(), # 테스트 용
            # 'major': lambda x: Major.objects.order_by('?').first(), # 학과 랜덤으로 신청
            'user': lambda x: User.objects.order_by('?').first(),
            'building_id': lambda x: Building.objects.filter(id__in=[1, 2]).order_by('?').first(),
            'priority_1_answer': lambda x: random.choice([True, False]),
            'priority_2_answer': lambda x: random.randint(1, 150),
            'priority_3_answer': None,
            'created_at': lambda x: fake.date_time_between(start_date='-3d', end_date='now')
        })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Apply data, Success!"))