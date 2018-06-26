from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    '''
    Command for granting permission
    '''
    help = 'grant or revoke permission to add users'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument(
            '--grant',
            action='store_true',
            dest='grant',
            help='Grant user permision to add users via API'
        )
        parser.add_argument(
            '--revoke',
            action='store_true',
            dest='revoke',
            help='Revoke permission to add users via API'
        )
    
    def handle(self, *args, **options):
        '''
        execute command
        '''

        username = options['username']
        revoke = options['revoke']
        grant = options['grant']

        # check user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError('user doesnot exist')
        
        if grant:
            if getattr(user.userprofile, 'can_create_users'):
                self.stdout.write(
                self.style.SUCCESS('"%s" already has rights to add users via rest api'%username))
            else:
                setattr(user.userprofile, 'can_create_users', True)
                user.userprofile.save()
                self.stdout.write(
                self.style.SUCCESS('"%s" now has rights to add users via rest api'%username))
            
        if revoke:
            if not getattr(user.userprofile, 'can_create_users'):
                self.stdout.write(
                self.style.SUCCESS('"%s" already has no rights to add users via rest api'%username))
            else:
                setattr(user.userprofile, 'can_create_users', False)
                user.userprofile.save()
                self.stdout.write(
                self.style.SUCCESS('"%s" now has no rights to add users via rest api'%username))
        
