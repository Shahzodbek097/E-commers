from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, Product, Baho


User = get_user_model()

class CategoryViewSetAPITest(APITestCase):     # python manage.py dumpdata products.Category --format=yaml --indent=2 > products/fixtures/category.yaml
    fixtures = ["category"]

    def SetUp(self):
        self.user=User.objects.create_user(username="Abbos", password="1234")
        self.client.force_authenticate(user=self.user)
        self.category1=Category.objects.first()

    def test_category_list(self):
        url=reverse('category-list')
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_detail(self):
        url=reverse('category-detail', kwargs=[self.category1.pk])
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_create(self):
        url=reverse('category-list')
        data={'name': 'mebellar'}
        response=self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_uptade(self):
        url=reverse('category-detail', kwargs=[self.category1.pk])
        data={'name': 'sabzavotlar'}
        response=self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_delete(self):
        url=reverse('category-detail', kwargs=[self.category1.pk])
        response=self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


