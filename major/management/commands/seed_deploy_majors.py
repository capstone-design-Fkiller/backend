from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from major.models import Major
from datetime import datetime
from major.models import Priority
import info

class Command(BaseCommand):
    help = 'Seed Major data'

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        majors = list(info.MAJORS.keys())

        user_test_majors = majors[:16]
        admin_test_majors = majors[16:]

        for major in user_test_majors :
            seeder.add_entity(Major, 1, {
                'name': major,
                'start_date' : "2023-7-1",
                'end_date' : "2023-8-1",
                'apply_start_date': "2023-6-1",
                'apply_end_date': "2023-6-20",
                'priority_1': Priority.objects.filter(name="학생회비 납부여부").first(),
                'priority_2': Priority.objects.filter(name="통학시간").first(),
                'priority_3': None
            })

        for major in admin_test_majors :
            seeder.add_entity(Major, 1, {
                'name': major,
                'start_date' : None,
                'end_date' : None,
                'apply_start_date': None,
                'apply_end_date': None,
                'priority_1': None,
                'priority_2': None,
                'priority_3': None
            })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Major data, Success!"))