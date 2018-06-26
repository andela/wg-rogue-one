from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from wger.core.models import RestAPIUsers

class Command(BaseCommand):
    '''
    Command for granting permission
    '''
    help = 'grant or revoke permission to add users'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument(
            '--username',
            action='store_true',
            dest='grant',
            help='List users created via API'
        )

    def handle(self, *args, **options):
        '''
        execute command
        '''
        username = options['username']
        # check user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError('user doesnot exist')
        
        # list users
        api_users = (user for user in RestAPIUsers.objects.filter(registered_by=user))
        for user in api_users:
            self.stdout.write("User: %s" % user.user)
