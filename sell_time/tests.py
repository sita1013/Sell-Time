from django.test import TestCase
from django.urls import reverse
from sell_time.models import TimePackage

class SimpleURLTests(TestCase):
    def test_homepage_url(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sell_time/homepage.html')

    def test_product_list_url(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sell_time/product_list.html')

    def test_cart_url(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sell_time/cart.html')

class TimePackageDuplicateTest(TestCase):
    def test_no_duplicate_timepackages(self):
        from collections import Counter
        key_list = list(
            TimePackage.objects.values_list('duration_minutes', 'use_type')
        )
        duplicates = [item for item, count in Counter(key_list).items() if count > 1]
        self.assertEqual(
            len(duplicates), 0,
            msg=f"Found duplicate TimePackages for: {duplicates}"
        )