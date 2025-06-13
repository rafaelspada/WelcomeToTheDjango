from django.core import mail
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

class SubscriblePostTest(TestCase):
    def setUp(self):
        data = dict(name='Rafael Spada', cpf='12345678901', email='spada@digisat.com', phone='49-99999-9999')
        self.resp = self.client.post('/inscricao/', data=data)

    def test_post(self):
        """validação de post para /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def teste_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expected = "Confirmação de inscrição"
        self.assertEqual(expected, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expected = 'contato@eventex.com.br'
        self.assertEqual(expected, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expected = ['contato@eventex.com.br','spada@digisat.com']
        self.assertEqual(expected, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]
        self.assertIn('Rafael Spada', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('spada@digisat.com', email.body)
        self.assertIn('Rafael Spada', email.body)