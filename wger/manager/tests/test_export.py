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
from django.core.urlresolvers import reverse

from wger.core.tests.base_testcase import WorkoutManagerTestCase


class WorkoutJsonTestCase(WorkoutManagerTestCase):
    '''
    Tests exporting a workout as json
    '''

    def test_export_json(self, fail=False):
        '''
        Helper function to test exporting a workout as a json
        '''
        self.user_login('admin')
        response = self.client.get(reverse('manager:workout:export_json', kwargs={'pk': 3}))

        if fail:
            self.assertIn(response.status_code, (403, 404, 302))
        else:
            self.assertEqual(response.status_code, 200)

    def test_view_imports(self):
        '''
            Helper function to test view of imported workout as a json
        '''
        self.user_login('admin')
        response = self.client.get(reverse('manager:workout:view_imports'))
        self.assertEqual(response.status_code, 200)

    def test_import_workout(self):
        '''
            Helper function to test adopting a workout imported
        '''
        self.user_login('admin')
        response = self.client.get(reverse('manager:workout:import_workout', kwargs={
                                   'imported_workout': '3', 'imported_from': 'admin'}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('manager:workout:view', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, 200)
