from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from major.models import Major
from locker.models import Locker, Building
import info

class Command(BaseCommand):
    help = 'Seed Locker data'

    def handle(self, *args, **options):
        majors = info.MAJORS
        buildings = Building.objects.all()

        seeder = Seed.seeder()
        for major_name, major_data in majors.items():
            # count = major_data['count']  # 학과별 사물함 개수
            lockers = major_data['lockers']  # 건물별 사물함 개수 (dictionary)
            # major = Major.objects.get(name=major_name)

            for building_floor, locker_count in lockers.items():
                building_num, floor = building_floor  # 건물 번호와 층 정보를 분리

                seeder.add_entity(
                    Locker,
                    locker_count,
                    {
                        'building_id': Building.objects.filter(id=building_num).first(),
                        'floor': floor,
                        'major': Major.objects.filter(name=major_name).first(),
                        'owned_id':None,
                        'shared_id':None,
                        'is_share_registered': False,
                        'start_date':None,
                        'end_date':None,
                        'share_start_date':None,
                        'share_end_date':None
                    }
                )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Locker data, Success!"))