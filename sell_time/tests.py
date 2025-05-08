from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from sell_time.models import TimePackage
from .models import TimePackage, Purchase
from decimal import Decimal

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

class TimePackageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_timepackage(self):
        package = TimePackage.objects.create(
            name='Test Package',
            description='Just a test package',
            duration_minutes=60,
            price=Decimal('60.00'),
            use_type='future',
            creator=self.user
        )
        self.assertEqual(str(package), 'Test Package')
        self.assertEqual(package.price, Decimal('60.00'))
        self.assertEqual(package.creator.username, 'testuser')

class PurchaseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass123')
        self.package = TimePackage.objects.create(
            name='Buyable Time',
            description='Purchased time block',
            duration_minutes=30,
            price=Decimal('30.00'),
            use_type='past',
            creator=self.user
        )

    def test_create_purchase(self):
        purchase = Purchase.objects.create(
            user=self.user,
            email='buyer@example.com',
            package=self.package,
            quantity=1
        )
        self.assertEqual(purchase.package.name, 'Buyable Time')
        self.assertEqual(purchase.email, 'buyer@example.com')
        self.assertEqual(purchase.quantity, 1)
