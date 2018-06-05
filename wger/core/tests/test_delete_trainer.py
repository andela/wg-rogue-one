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

import logging

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.core.models import UserProfile

logger = logging.getLogger(__name__)


class DeleteTrainerByAdminTestCase(WorkoutManagerTestCase):
    '''
    Tests deleting a trainer from gym by the gym admin
    '''

    def delete_trainer(self, fail=False):
        '''
        Helper function
        '''
        response = self.client.get(reverse('core:user:delete_trainer',
                                           kwargs={'user_pk': 2, 'gym_pk': 1}))
        self.assertEqual(User.objects.filter(username='test').count(), 1)
        if fail:
            self.assertIn(response.status_code, (302, 403),
                          'Unexpected status code for user {0}'.format(self.current_user))
        else:
            self.assertEqual(response.status_code, 200,
                             'Unexpected status code for user {0}'.format(self.current_user))

        # Wrong admin password
        if not fail:
            response = self.client.post(reverse('core:user:delete_trainer',
                                                kwargs={'user_pk': 2, 'gym_pk': 1}),
                                        {'password': 'blargh'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(User.objects.filter(username='test').count(), 1)

        # Correct user password
        response = self.client.post(reverse('core:user:delete_trainer',
                                            kwargs={'user_pk': 2, 'gym_pk': 1}),
                                    {'password': self.current_password})
        if fail:
            self.assertIn(response.status_code, (302, 403))
            self.assertEqual(User.objects.filter(username='test').count(), 1)
        else:
            self.assertEqual(response.status_code, 302)
            self.assertEqual(User.objects.filter(username='test').count(), 1)
            self.assertEqual(UserProfile.objects.get(user=2).gym, None)

    def test_delete_trainer_manager(self):
        '''
        Tests deleting trainer as a gym manager
        '''
        self.user_login('manager1')
        self.delete_trainer(fail=False)

    def test_delete_trainer_manager2(self):
        '''
        Tests deleting trainer as a gym manager
        '''
        self.user_login('manager2')
        self.delete_trainer(fail=False)

    def test_delete_trainer_general_manager(self):
        '''
        Tests deleting trainer as a general manager
        '''
        self.user_login('general_manager1')
        self.delete_trainer(fail=False)

    def test_delete_trainer_general_manager2(self):
        '''
        Tests deleting trainer as a general manager
        '''
        self.user_login('general_manager2')
        self.delete_trainer(fail=False)

    def test_delete_trainer(self):
        '''
        Tests deleting trainer as a regular user
        '''
        self.user_login('test')
        self.delete_trainer(fail=True)

    def test_delete_trainer_trainer(self):
        '''
        Tests deleting trainer as a gym trainer
        '''
        self.user_login('trainer1')
        self.delete_trainer(fail=True)

    def test_delete_trainer_trainer2(self):
        '''
        Tests deleting trainer as a gym trainer
        '''
        self.user_login('trainer4')
        self.delete_trainer(fail=True)

    def test_delete_trainer_trainer_other(self):
        '''
        Tests deleting trainer as a gym trainer of another gym
        '''
        self.user_login('trainer4')
        self.delete_trainer(fail=True)

    def test_delete_trainer_manager_other(self):
        '''
        Tests deleting trainer as a gym manager of another gym
        '''
        self.user_login('manager3')
        self.delete_trainer(fail=True)

    def test_delete_trainer_member(self):
        '''
        Tests deleting trainer as a gym member
        '''
        self.user_login('member1')
        self.delete_trainer(fail=True)

    def test_delete_trainer_anonymous(self):
        '''
        Tests deleting trainer as an anonymous user
        '''
        self.delete_trainer(fail=True)
