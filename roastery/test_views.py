from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Category, CoffeeOrigin, CoffeeGrind, CoffeeSize

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(main_category='Beverage')
        self.origin = CoffeeOrigin.objects.create(continent=0, country=0, region=0)
        self.grind = CoffeeGrind.objects.create(grind=0)
        self.size = CoffeeSize.objects.create(size=250, unit='g')
        self.product = Product.objects.create(
            category=self.category,
            origin_id=self.origin,
            grind_id=self.grind,
            size_id=self.size,
            manufacturer='Acme Corp',
            name='Premium Coffee',
            description='The best coffee in town.',
            price=20.00,
            currency='USD',
            image='static/images/coffee/relish_test_image.webp'
        )

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('continent_list', response.context)

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roastery/product_list.html')
        self.assertIn('products', response.context)

    def test_origin_products_view(self):
        response = self.client.get(reverse('origin_products', args=['African']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'origin_products.html')
        self.assertIn('products', response.context)

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertIn('product', response.context)

    def test_purchase_form_view(self):
        response = self.client.get(reverse('purchase_form', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'purchase_form.html')
        self.assertIn('form', response.context)
        self.assertIn('product', response.context)

    def test_success_page_view(self):
        response = self.client.get(reverse('success_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success_page.html')

    def test_create_product_view_get(self):
        response = self.client.get(reverse('create_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roastery/product_form.html')
        self.assertIn('form', response.context)

    def test_create_product_view_post(self):
        image_path = 'static/images/coffee/relish_test_image.webp'
        with open(image_path, 'rb') as f:
            image_file = SimpleUploadedFile(f.name, f.read(), content_type='image/webp')

        form_data = {
            'category': self.category.category_id,
            'origin_id': self.origin.origin_id,
            'grind_id': self.grind.grind_id,
            'size_id': self.size.size_id,
            'manufacturer': 'New Manufacturer',
            'name': 'New Coffee',
            'description': 'A new coffee product.',
            'price': '25.00',
            'currency': 'USD',
            'image': image_file
        }
        response = self.client.post(reverse('create_product'), data=form_data, format='multipart')
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation

    def test_update_product_view_get(self):
        response = self.client.get(reverse('update_product', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roastery/product_form.html')
        self.assertIn('form', response.context)

    def test_update_product_view_post(self):
        image_path = 'static/images/coffee/relish_test_image.webp'
        with open(image_path, 'rb') as f:
            image_file = SimpleUploadedFile(f.name, f.read(), content_type='image/webp')

        form_data = {
            'category': self.category.category_id,
            'origin_id': self.origin.origin_id,
            'grind_id': self.grind.grind_id,
            'size_id': self.size.size_id,
            'manufacturer': 'Updated Manufacturer',
            'name': 'Updated Coffee',
            'description': 'An updated coffee product.',
            'price': '30.00',
            'currency': 'USD',
            'image': image_file
        }
        response = self.client.post(reverse('update_product', args=[self.product.product_id]), data=form_data, format='multipart')
        self.assertEqual(response.status_code, 302)  # Redirect after successful update

    def test_delete_product_view_get(self):
        response = self.client.get(reverse('delete_product', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roastery/product_confirm_delete.html')
        self.assertIn('product', response.context)

    def test_delete_product_view_post(self):
        response = self.client.post(reverse('delete_product', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Product.objects.filter(product_id=self.product.product_id).exists())
