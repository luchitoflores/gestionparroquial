"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from .models import PerfilUsuario

class ViewSacramentosTestLogin(TestCase):

	def setUp(self):
		self.client = Client()
		user = User.objects.create_user('loco', 'loco@gmail.com', 'loco')
		self.client.login(username='admin', password='admin')

	def test_view_add_feligres(self):
		response = self.client.get('/usuario/')
		self.assertEqual(response.status_code, 200)

	def test_view_add_administrador(self):
		response = self.client.get('/administrador/add/')
		self.assertEqual(response.status_code, 200)

	def test_view_home(self):
		response = self.client.get('/home/')
		self.assertEqual(response.status_code,200)

	def test_view_index(self):
		response = self.client.get('/administrador/add/')
		self.assertEqual(response.status_code, 200)


class ViewSacramentosTestLogout(TestCase):
	def setUp(self):
		self.client = Client()

	def test_view_add_feligres(self):
		response = self.client.get('/usuario/')
		self.assertEqual(response.status_code, 403)

	def test_view_add_administrador(self):
		response = self.client.get('/administrador/add/')
		self.assertEqual(response.status_code, 403)

	def test_view_home(self):
		response = self.client.get('/home/')
		self.assertEqual(response.status_code,403)

	def test_view_index(self):
		response = self.client.get('/administrador/add/')
		self.assertEqual(response.status_code, 200)
