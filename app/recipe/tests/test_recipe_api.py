"""
Tests the recipe API
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')
def create_recipe(user, **params):
    """Create and return a smaple recipe"""
    defaults = {
        'title':'Sample Recipe Title',
        'time_minutes':22,
        'price':Decimal('5.25'),
        'description': 'Sample Description',
        'link': 'http://example.com/recipe.pdf'
    }
    default.update(params)

    recipe = Recipe.objects,create(user = user, **defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """Test unauthorized api tests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call api"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',

        )
        self.client = APIClient()
        self.client.force_authenticate(user = self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res=self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, Many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data , serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Tests list of recipes is limited to authenticated user"""
        other_user = self.user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',

        )
        create_recipe(user = other_user)
        create_recipe(user = self.user)

        res= self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes, Many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data , serializer.data)
