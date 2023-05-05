from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from major.models import Major
from itertools import cycle

from user.models import User

class Command(BaseCommand):
    help = 'Seed User data'

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--total",
    #         default=3,
    #         type=int,
    #         help="몇 개의 유저를 만드는지"
    #     )

    #     return

    def handle(self, *args, **options):

        names = ['최희락', '최성민', '유지민', '정나윤', '손명근']
        ids = ['2016', '2017', '2018', '2019', '201801910']
        majors= [24, 4, 19, 24, 17]
        # passwords = [] # 프론트에서 암호화해서 넘겨주면 암호화된 키 값들로 또 암호화해야함.

        for i in range(len(names)):
            id = ids[i]
            password = 'qwer1234!' # 프론트 암호화 키로 변경 예정
            name = names[i]
            major=Major.objects.filter(pk=majors[i]).first()
            is_usermode = True
            User.objects.create_user(id=id, password=password, name=name, major=major, is_usermode=is_usermode)

        self.stdout.write(self.style.SUCCESS("Success!"))