import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from user.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):


        user_seeder = Seed.seeder()
        user_seeder.add_entity(
            User,
            2,
            {
                "name": lambda x: user_seeder.faker.name(),
                "password" : lambda x: user_seeder.faker.password(),
                "created_at" : lambda x: user_seeder.faker.date()
            }
        )
        user_seeder.execute()