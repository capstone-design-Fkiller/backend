from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from major.models import Major
from itertools import cycle

class Command(BaseCommand):
    help = 'Seed User data'

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--total",
    #         default=3,
    #         type=int,
    #         help="몇 개의 전공을 만드는지"
    #     )

    #     return

    def handle(self, *args, **options):
        # total = options.get("tatal")
        seeder = Seed.seeder()

        # 학과개수 32개
        names = cycle(['프랑스어학부','독일어과','노어과','스페인어과','이탈리아어과',
                       '포르투갈어과','네덜란드어과','스칸디나비아어과','말레이인도네시아어과','아랍어과',
                       '태국어과','베트남어과','인도어과','터키아제르바이잔어과','페르시아어이란학과',
                       '몽골어과','ELLT학과','영미문학문화학과','EICC','중국학대학',
                       '일본학대학','정치외교학과','행정학과','영어교육과','한국어교육과',
                       '프랑스어교육과','독일어교육과','중국어교육과','상경대학','경영학부',
                       '국제학부',"LD학부"])

        seeder.add_entity(Major, 32, {
            'name': lambda x: next(names),
            'apply_start_date': None,
            'apply_end_date': None,
            'priority_first': None,
            'priority_second': None,
            'priority_third': None,
        })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Success!"))