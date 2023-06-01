from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from major.models import Major
from datetime import datetime
from major.models import Priority
import info

class Command(BaseCommand):
    help = 'Seed Priority data'

    def handle(self, *args, **options):
        names = ['학생회비 납부여부','재학여부','통학여부','통학시간','고학번','전공수업수']
        questions = ['학생회비를 납부하셨습니까?',
                     '재학생입니까?',
                     '통학생입니까?',
                     '분, 숫자만 입력',
                     '두자리 숫자만 입력',
                     '개, 숫자만 입력']
        is_bools = [True, True, True, False, False, False]
        is_ascendings = [False, False, False, False, True, False]

        for i in range(len(names)) :
            seeder = Seed.seeder()
            seeder.add_entity(Priority, 1, {
                'name': names[i],
                'question': questions[i],
                'is_bool': is_bools[i],
                'is_ascending': is_ascendings[i],
            })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Priority data, Success!"))