import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings")
import django
django.setup()


from products.models import Product, ProductCategory
from http import HTTPStatus
from django.urls import reverse
from django.test import TestCase



class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
      #  self.assertTemplateUsed(response, 'products\index.html')


class ProductsListViewTestCase(TestCase):

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        fixtures = ['categories.json', 'goods.json']
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(list(response.context_data['object_list']),
                         list(self.products.filter(category_id=category.id)))

    def _common_test(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Каталог')
        # self.assertTemplateUsed(response, 'products\products.html')
