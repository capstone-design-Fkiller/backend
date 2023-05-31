from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from major.models import Major
from locker.models import Locker, Building
import info

class Command(BaseCommand):
    help = 'Seed Locker data'

    def handle(self, *args, **options):
        majors = Major.objects.all()

        for major in majors:
            lockers = Locker.objects.filter(major=major).order_by('id')

            for i, locker in enumerate(lockers):
                locker.locker_number = i + 1
                locker.save()

        self.stdout.write(self.style.SUCCESS("Modify locker_number, Success!"))