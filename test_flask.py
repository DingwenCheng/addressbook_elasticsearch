import unittest
from unittest import TestCase
import addr_book_flask


class Test_Flask(TestCase):
    def setUp(self):
        addr_book_flask.app.testing = True
        self.app = addr_book_flask.app.test_client()

    def tearDown(self):
        pass

    def test_1_get_fail(self):
        res = self.app.get('/contact/Troy')
        self.assertEqual(res.status_code, 400)

    # def test_2_get_fail(self):
    #     query = {}
    #     res = self.app.get('/contact?pageSize=3&page=2&query=Bob')
    #     self.assertEqual(res.status_code, 400)

    def test_3_post(self):
        res1 = self.app.post('/contact', data={"name": "Bob", "address": "1street", "phone": "1234567890"})
        res2 = self.app.post('/contact', data={"name": "Bob", "address": "1street", "phone": "1234567890"}) # duplicate fail
        res3 = self.app.post('/contact', data={"name": "Amy", "address": "2street", "phone": "2234567890"})
        res4 = self.app.post('/contact', data={"address": "1street", "phone": "1234567890"}) # missing name fail
        res5 = self.app.post('/contact', data={"name": "Henry", "address": "1street", "phone": "1234567890123456789"}) # phone too long fail
        res6 = self.app.post('/contact', data={"name": "CN", "address": "3street", "phone": "1234567890"})
        res7 = self.app.post('/contact', data={"name": "BT", "address": "1street", "phone": "a1234567890"}) # phone with alphabets fail
        res8 = self.app.post('/contact', data={"name": "Andy", "address": "4street", "phone": "1234567890"})
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 400)
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(res4.status_code, 400)
        self.assertEqual(res5.status_code, 400)
        self.assertEqual(res6.status_code, 200)
        self.assertEqual(res7.status_code, 400)
        self.assertEqual(res8.status_code, 200)

    def test_4_get_one(self):
        res1 = self.app.get('/contact/Bob')
        res2 = self.app.get('/contact/Amy')
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)

    def test_5_put(self):
        res1 = self.app.put('/contact/Bob', data={"address": "5street", "phone": "22222222222"})
        res2 = self.app.put('/contact/Amy', data={"phone": "22222222222"})
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)

    def test_6_query(self):
        res1 = self.app.get('/contact?pageSize=3&page=1&query=Bob')
        res2 = self.app.get('/contact?pageSize=3&page=4&query=Bob') # page number too big fail
        res3 = self.app.get('/contact?pageSize=3&page=1&query=Bob+Amy')
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 400)
        self.assertEqual(res3.status_code, 200)

    def test_7_delete(self):
        res1 = self.app.delete('/contact/Andy')
        res2 = self.app.delete('/contact/Test') # name not found fail
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 400)


if __name__ == '__main__':
    unittest.main()
