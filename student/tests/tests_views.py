from rest_framework import status
from student.models import Student, Subject, Parent, Token, User
from django.test import TestCase


class ProductDetailTest(TestCase):

    def setUp(self):
        self.ep = '/api/parents/'

    def test_get_product_detail_not_found(self):

        response = self.client.post(self.ep,
                                    {
                                        "first_name": "Akram",
                                        "last_name": "Abdelfattah",
                                        "username": "akram",
                                        "password": "1234"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)