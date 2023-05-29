from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from major.models import Major
from locker.models import Locker, Building
from user.models import User
import info

class Command(BaseCommand):
    help = 'Share Locker data'

    def handle(self, *args, **options):
        user = User.objects.get(id=2017)
        major = Major.objects.get(id=4) #스페인어과
        lockers = Locker.objects.filter(major=major)

        for locker in lockers :
            locker.is_share_registered = True
            locker.owned_id = user
            locker.share_start_date = '2023-05-01'
            locker.share_end_date = '2023-07-01'
            locker.save()

        self.stdout.write(self.style.SUCCESS("Share Locker data, Success!"))