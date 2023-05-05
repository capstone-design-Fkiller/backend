from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from major.models import Major
from locker.models import Locker, Building
import info

class Command(BaseCommand):
    help = 'Seed Building data'

    def handle(self, *args, **options):
        building = info.BUILDINGS
        seeder = Seed.seeder()

        for building_name,building_id in building.items() :
            seeder.add_entity(Building, 1, {
                'id':building_id,
                'name': building_name
            })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS("Building data, Success!"))