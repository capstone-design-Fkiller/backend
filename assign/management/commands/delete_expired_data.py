from django.core.management.base import BaseCommand, CommandParser
from major.models import Major
from assign.views import AssignAPIView
from django.utils import timezone
from apply.models import Apply
from apply.views import ApplyDetail

class Command(BaseCommand):
    # 배포용으로 전체삭제를 만든것임
    help = 'Delete assign Data'

    def handle(self, *args, **options):
        majors = Major.objects.all()
        for major in majors:
            # assign 데이터 전체 삭제
            AssignAPIView().delete(None, major=major.pk)

        # apply 데이터 전체 삭제    
        applies = Apply.objects.all()
        for apply in applies:
            ApplyDetail().delete(None, pk=apply.id)

        self.stdout.write(self.style.SUCCESS("Delete Apply & Assign Data!"))