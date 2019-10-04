from django.test import TestCase

class OurTest(TestCase):
    def setUp(self):
        pass
    def test_insert(self):
        self.assertEquals('123','123')
    def tearDown(self):
        pass

# Create your tests here.
