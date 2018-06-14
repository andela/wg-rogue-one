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


import datetime
from django.core.cache import cache
from wger.utils.cache import cache_mapper
from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.nutrition.models import NutritionPlan


class NutritionInfoCacheTestCase(WorkoutManagerTestCase):
    '''
    Test case for the nutritional values caching
    '''

    def test_meal_nutritional_values_cache(self):
        '''
        Tests that the nutrition cache of the canonical form is
        correctly generated
        '''
        self.assertFalse(cache.get(cache_mapper.get_nutritional_values_canonical(1)))

        plan = NutritionPlan.objects.get(pk=1)
        plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_values_canonical(1)))

    def test_nutritional_values_cache_save(self):
        '''
        Tests nutritional values cache when saving
        '''
        plan = NutritionPlan.objects.get(pk=1)
        plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_values_canonical(1)))

        plan.save()
        self.assertFalse(cache.get(cache_mapper.get_nutritional_values_canonical(1)))

    def test_nutritional_values_cache_delete(self):
        '''
        Tests the nutritional values cache when deleting
        '''
        plan = NutritionPlan.objects.get(pk=1)
        plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_values_canonical(1)))

        plan.delete()
        self.assertFalse(cache.get(cache_mapper.get_nutritional_values_canonical(1)))
