from django.core.management.base import BaseCommand
from apply.models import Apply
from apply.models import Sort

class Command(BaseCommand):
    help = 'Sort Apply data'

    def handle(self, *args, **options):
        applies = Apply.objects.all().order_by(
            '-priority_1_answer',
            '-priority_2_answer',
            '-priority_3_answer',
            'created_at'
        )

        Sort.objects.all().delete()  # 기존 Sort 데이터 삭제

        for priority, apply in enumerate(applies, start=1):
            sort_instance = Sort(
                priority=priority,
                apply=apply,
                building_id=apply.building_id,
                created_at=apply.created_at,
                major=apply.major,
                priority_1_answer=apply.priority_1_answer,
                priority_2_answer=apply.priority_2_answer,
                priority_3_answer=apply.priority_3_answer
            )
            sort_instance.save()

        self.stdout.write(self.style.SUCCESS("Apply data sorted successfully!"))