from django.core.management.base import NoArgsCommand
from main import add_groups

class Command(NoArgsCommand):
    help = "Creates required user groups for AtYourService"

    def handle_noargs(self, **options):
        add_groups(None)
