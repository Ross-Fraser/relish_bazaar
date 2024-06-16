from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from .forms import SignUpForm
from django.urls import reverse

class SignUpFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_no_email(self):
        form_data = {
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_invalid_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'weakpassword123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_invalid_form_existing_user(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='password123')
        form_data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
class PasswordResetFormTest(TestCase):
    def test_password_reset_form(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

        # Ensure email input field is present
        self.assertContains(response, 'id="id_email"', count=1)
        self.assertContains(response, 'type="email"', count=1)

        # Ensure CSRF token is present
        self.assertContains(response, 'csrfmiddlewaretoken')

        # Ensure submit button is present
        self.assertContains(response, '<button', count=1)
        self.assertContains(response, 'type="submit"', count=1)
        self.assertContains(response, 'Reset my password')

        # Ensure form is using POST method
        self.assertContains(response, 'method="post"')