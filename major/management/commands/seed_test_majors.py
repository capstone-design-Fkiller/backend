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

        for major in info.MAJORS :
            seeder.add_entity(Major, 1, {
                'name': major,
                'start_date' : None,
                'end_date' : None,
                'apply_start_date': "2023-3-1",
                'apply_end_date': "2023-6-20",
                'priority_1': Priority.objects.filter(name="학생회비 납부여부").first(),
                'priority_2': Priority.objects.filter(name="통학시간").first(),
                'priority_3': None
            })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Major data, Success!"))