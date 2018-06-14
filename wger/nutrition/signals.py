# -*- coding: utf-8 -*-

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


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from wger.nutrition.models import NutritionPlan, Meal, MealItem
from wger.utils.cache import reset_nutritional_values_canonical_form


@receiver(post_save, sender=NutritionPlan)
@receiver(post_save, sender=Meal)
@receiver(post_save, sender=MealItem)
@receiver(post_delete, sender=NutritionPlan)
@receiver(post_delete, sender=Meal)
@receiver(post_delete, sender=MealItem)
def delete_cache(sender, **kwargs):
    """ Function for intercepting signals """

    sender_instance = kwargs['instance']
    if sender == NutritionPlan:
        pk = sender_instance.pk
    elif sender == Meal:
        pk = sender_instance.plan.pk
    elif sender == MealItem:
        pk = sender_instance.meal.plan.pk

    reset_nutritional_values_canonical_form(pk)
