from django.core.management.base import BaseCommand, CommandParser
from major.models import Major
from assign.views import AssignAPIView
from django.utils import timezone
from apply.models import Apply
from apply.views import ApplyDetail

class Command(BaseCommand):
    help = 'Delete assign Data'

    def handle(self, *args, **options):
        expired_majors = Major.objects.filter(end_date__lte=timezone.now())
        for major in expired_majors:
            if major.end_date and major.end_date <= timezone.now():
                # assign 데이터 삭제
                AssignAPIView().delete(None, major=major.pk)

            # apply 데이터 삭제    
            applies = Apply.objects.filter(major=major)
            for apply in applies:
                ApplyDetail().delete(None, pk=apply.id)

        self.stdout.write(self.style.SUCCESS("Delete Apply & Assign Data!"))