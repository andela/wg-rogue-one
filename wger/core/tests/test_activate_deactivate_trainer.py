# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy

from wger.core.tests.base_testcase import (
    WorkoutManagerTestCase
)
from wger.core.models import UserProfile


class StatusTrainerTestCase(WorkoutManagerTestCase):
    '''
    Test activating and deactivating trainer
    '''
    user_success = ('general_manager1',
                    'general_manager2',
                    'manager1',
                    'manager2',

                    )

    user_fail = ('member1',
                 'member2',
                 'member3',
                 'trainer4',
                 )

    def activate_trainer(self, fail=False):
        '''
        Helper function to test activating trainer
        '''
        trainer = UserProfile.objects.get(pk=4, gym=1)
        trainer.is_activated = False
        trainer.save()
        self.assertFalse(trainer.is_activated)

        response = self.client.get(reverse('core:user:activate_trainer',
                                           kwargs={'user_pk': 4, 'gym_pk': 1}))
        trainer = UserProfile.objects.get(pk=4, gym=1)

        self.assertIn(response.status_code, (302, 403))
        if fail:
            self.assertFalse(trainer.is_activated)
        else:
            self.assertTrue(trainer.is_activated)

    def test_activate_authorized(self):
        '''
        Tests activating a trainer as an administrator
        '''
        for username in self.user_success:
            self.user_login(username)
            self.activate_trainer()
            self.user_logout()

    def test_activate_unauthorized(self):
        '''
        Tests activating a trainer as another logged in user
        '''
        for username in self.user_fail:
            self.user_login(username)
            self.activate_trainer(fail=True)
            self.user_logout()

    def test_activate_logged_out(self):
        '''
        Tests activating a trainer as logged out user
        '''
        self.activate_trainer(fail=True)

    def deactivate_trainer(self, fail=False):
        '''
        Helper function to test deactivating trainer
        '''
        trainer = UserProfile.objects.get(pk=4, gym=1)
        trainer.is_activated = True
        trainer.save()
        self.assertTrue(trainer.is_activated)

        response = self.client.get(reverse('core:user:deactivate_trainer',
                                           kwargs={'user_pk': 4, 'gym_pk': 1}))
        trainer = UserProfile.objects.get(pk=4, gym=1)

        self.assertIn(response.status_code, (302, 403))
        if fail:
            self.assertTrue(trainer.is_activated)
        else:
            self.assertFalse(trainer.is_activated)

    def test_deactivate_authorized(self):
        '''
        Tests deactivating a trainer as an administrator
        '''
        for username in self.user_success:
            self.user_login(username)
            self.deactivate_trainer()
            self.user_logout()

    def test_deactivate_unauthorized(self):
        '''
        Tests deactivating a trainer as another logged in user
        '''
        for username in self.user_fail:
            self.user_login(username)
            self.deactivate_trainer(fail=True)
            self.user_logout()

    def test_deactivate_logged_out(self):
        '''
        Tests deactivating a trainer as logged out user
        '''
        self.deactivate_trainer(fail=True)
