
from django.core.management.base import BaseCommand, CommandParser
from locker.models import Locker
from major.models import Major
from assign.views import AssignAPIView
from django.utils import timezone
from apply.models import Apply
from apply.views import ApplyDetail

class Command(BaseCommand):
    help = 'Patch shared locker'

    def handle(self, *args, **options):
        lockers = Locker.objects.filter(is_share_registered=1)
        for locker in lockers:
            print(locker.id)
            # assign 데이터 삭제
            locker.share_start_date = None
            locker.share_end_date = None
            locker.shared_id = None
            locker.is_share_registered = False

            locker.save()

        self.stdout.write(self.style.SUCCESS("Patch shared locker!"))