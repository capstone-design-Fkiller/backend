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
                'apply_start_date': None,
                'apply_end_date': None,
                'priority_1': None,
                'priority_2': None,
                'priority_3': None
            })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Major data, Success!"))