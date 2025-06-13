from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscriptionsTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscrição/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ subscriptions/subscription_form.html """
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """ Html must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"', 1)
        self.assertContains(self.resp, 'type="submit"', 1)

    def test_csrf(self):
        """constain CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def teste_as_form(self):
        """" subscription form """
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name','cpf','email','phone'], list(form.fields))