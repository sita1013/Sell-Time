from django.test import TestCase
from django.urls import reverse

class SimpleURLTests(TestCase):
    def test_homepage_url(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sell_time/homepage.html')

    def test_product_list_url(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sell_time/product_list.html')

    def test_graphs_url(self):
        response = self.client.get(reverse('graphs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sell_time/graphs.html')

    def cart_url(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sell_time/cart.html')

