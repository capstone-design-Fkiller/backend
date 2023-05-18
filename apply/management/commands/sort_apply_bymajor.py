from django.core.management.base import BaseCommand
from apply.models import Apply, Sort
from major.models import Major
from django.db import connections
from django.db import connection
from django.db import models


class Command(BaseCommand):
    help = 'Sort and store Apply data for a specific Major'

    def add_arguments(self, parser):
        parser.add_argument('major_id', type=int, help='ID of the Major')

    def handle(self, *args, **options):
        major_id = options['major_id']

        try:
            major = Major.objects.get(id=major_id)
        except Major.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Major with ID {major_id} does not exist"))
            return

        applies = Apply.objects.filter(major=major)

        is_ascending_1 = major.priority_1.is_ascending if major.priority_1 else None
        is_ascending_2 = major.priority_2.is_ascending if major.priority_2 else None
        is_ascending_3 = major.priority_3.is_ascending if major.priority_3 else None

        if applies.exists():

            if is_ascending_1 == None :
                sorted_applies = applies.order_by(
                    'created_at'
                )
            elif is_ascending_2 == None :
                sorted_applies = applies.order_by(
                    (f'priority_{1}_answer' if is_ascending_1 else f'-priority_{1}_answer'),
                    'created_at'
                )
            elif is_ascending_3 == None:
                sorted_applies = applies.order_by(
                    (f'priority_{1}_answer' if is_ascending_1 else f'-priority_{1}_answer'),
                    (f'priority_{2}_answer' if is_ascending_2 else f'-priority_{2}_answer'),
                    'created_at'
                )
            else :
                sorted_applies = applies.order_by(
                    (f'priority_{1}_answer' if is_ascending_1 else f'-priority_{1}_answer'),
                    (f'priority_{2}_answer' if is_ascending_2 else f'-priority_{2}_answer'),
                    (f'priority_{3}_answer' if is_ascending_3 else f'-priority_{3}_answer'),
                    'created_at'
                )

            # 새로운 Sort 테이블 생성
            sort_table_name = f"{major.name}_sort"

            # 이미 존재하는 테이블인 경우 삭제
            with connection.cursor() as cursor:
                cursor.execute(f"DROP TABLE IF EXISTS {sort_table_name};")

            # 테이블 생성
            Sort._meta.db_table = sort_table_name
            Sort._meta.model_name = sort_table_name
            Sort._meta.db_table = sort_table_name
            Sort._meta.db_tablespace = ''

            with connections['default'].schema_editor() as schema_editor:
                schema_editor.create_model(Sort)

            # 정렬된 데이터를 새로운 테이블에 저장
            for priority, apply in enumerate(sorted_applies, start=1):
                sort_instance = Sort(
                    priority=priority,
                    apply=apply,
                    user=apply.user,
                    building_id=apply.building_id,
                    created_at=apply.created_at,
                    major=apply.major,
                    priority_1_answer=apply.priority_1_answer,
                    priority_2_answer=apply.priority_2_answer,
                    priority_3_answer=apply.priority_3_answer
                )
                sort_instance.save()

            self.stdout.write(self.style.SUCCESS(f"Apply data for Major '{major.name}' sorted and stored successfully"))
        else:
            self.stdout.write(self.style.WARNING(f"No Apply data found for Major '{major.name}'"))