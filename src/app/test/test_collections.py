from django.test import TestCase
from app.models import CustomUser
import json

test_users = [
    {"username": "testuser1", "password": "testpassword1", "email": "t1@g.com"},
    {"username": "testuser2", "password": "testpassword2", "email": "t2@g.com"},
]

test_tokens = [{'tokenId': '1', 'name': 'token 1', 'image': 'http://img1'},
               {'tokenId': '2', 'name': 'token 2', 'image': 'http://img2'},
               {'tokenId': '3', 'name': 'token 3', 'image': 'http://img3'}]

test_collections = [
    {
        'collectionName': 'Custom Collection Name #1',
        'tokensList': test_tokens
    },
    {
        'collectionName': 'Custom Collection Name #2',
        'tokensList': test_tokens[:2]
    }
]


class CollectionsCRUDTest(TestCase):
    def setUp(self):
        for user in test_users:
            new_user = CustomUser.objects.create(username=user["username"])
            new_user.set_password(user["password"])
            new_user.save()

    def get_token(self, user):
        res = self.client.post('/api/token/',
                               data=json.dumps({
                                   'username': user["username"],
                                   'password': user["password"],
                               }),
                               content_type='application/json',
                               )
        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)
        return result['access']

    def test_create_collection_forbidden(self):
        res = self.client.post('/api/collections/',
                               data=json.dumps(test_collections[0]),
                               content_type='application/json',
                               )
        self.assertEquals(res.status_code, 401)
        res = self.client.post('/api/collections/',
                               data=json.dumps(test_collections[0]),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer WRONG TOKEN'
                               )
        self.assertEquals(res.status_code, 401)
        res = self.client.get('/api/collections/',
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer WRONG TOKEN'
                               )
        self.assertEquals(res.status_code, 401)

    def test_add_collection_ok(self):
        token = self.get_token(test_users[0])
        res = self.client.post('/api/collections/',
                               data=json.dumps(test_collections[0]),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        result = json.loads(res.content)["data"]
        result_fields = ['id', 'user', 'name',
                         'token_count', 'date_added', 'last_updated']
        self.assertTrue(sorted(list(result_fields)) ==
                        sorted(list(result.keys())))
        self.assertEqual(result['user'], 1)
        self.assertEqual(result['name'], 'Custom Collection Name #1')
        self.assertTrue(result['token_count'], len(
            test_collections[0]['tokensList']))

        created_collection_id = result['id']

        one_collection_res = self.client.get('/api/collections/' + str(created_collection_id) + '/',
                                             content_type='application/json',
                                             HTTP_AUTHORIZATION=f'Bearer {token}'
                                             )
        self.assertEquals(one_collection_res.status_code, 200)
        one_collection_result = json.loads(one_collection_res.content)["data"]

        collections_res = self.client.get('/api/collections/',
                                          content_type='application/json',
                                          HTTP_AUTHORIZATION=f'Bearer {token}'
                                          )
        self.assertEquals(collections_res.status_code, 200)
        collections_result = json.loads(collections_res.content)["data"]
        del one_collection_result['tokens']
        self.assertTrue(
            any(x == one_collection_result for x in collections_result['collections']))

    def test_add_collection_wrong_data(self):
        token = self.get_token(test_users[0])
        res = self.client.post('/api/collections/',
                               data=json.dumps({
                                   'collectionName': 'asd',
                                   'tokensList': []
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 400)

        res = self.client.post('/api/collections/',
                               data=json.dumps({
                                   'name': ''
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 400)

        res = self.client.post('/api/collections/',
                               data=json.dumps({
                                   'collectionName': 11,
                                   'tokensList': test_tokens
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 400)

        res = self.client.post('/api/collections/',
                               data=json.dumps({
                                   'collectionName': 'name',
                                   'tokensList': [{}]
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 400)

        res = self.client.post('/api/collections/',
                               data=json.dumps({
                                   'collectionName': 'name',
                                   'tokensList': [{'tokenId': 1, 'name': 'name', 'image': 'asd'}]
                               }),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 400)

    def test_edit_collection(self):
        token = self.get_token(test_users[0])
        res = self.client.post('/api/collections/',
                               data=json.dumps(test_collections[0]),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        result = json.loads(res.content)["data"]
        result_fields = ['id', 'user', 'name',
                         'token_count', 'date_added', 'last_updated']
        self.assertTrue(sorted(list(result_fields)) ==
                        sorted(list(result.keys())))
        # self.assertEqual(result['user'], 1)
        self.assertEqual(result['name'], 'Custom Collection Name #1')
        self.assertTrue(result['token_count'], len(
            test_collections[0]['tokensList']))

        created_collection_id = result['id']

        res = self.client.post('/api/collections/' + str(created_collection_id) + '/',
                               data=json.dumps(test_collections[1]),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 405)  # Post not allowed
        self.assertEquals(json.loads(res.content)[
                          'detail'], 'Method "POST" not allowed.')

        res = self.client.put('/api/collections/' + str(created_collection_id) + '/',
                              data=json.dumps(test_collections[1]),
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)["data"]
        result_fields = ['id', 'user', 'name',
                         'token_count', 'date_added', 'last_updated']
        self.assertTrue(sorted(list(result_fields)) ==
                        sorted(list(result.keys())))
        self.assertEqual(result['name'], 'Custom Collection Name #2')
        self.assertTrue(result['token_count'], len(
            test_collections[1]['tokensList']))

        res = self.client.get('/api/collections/' + str(created_collection_id) + '/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 200)
        new_result = json.loads(res.content)["data"]
        result['last_updated'] = result['last_updated'][:10]
        for i in range(max(len(new_result['tokens']), len(test_collections[1]['tokensList']))):
            for field in ('tokenId', 'image', 'name'):
                self.assertEqual(new_result['tokens'][i][field],
                                 test_collections[1]['tokensList'][i][field])
        del new_result['tokens']
        self.assertEqual(result, new_result)

    def test_delete_collection(self):
        token = self.get_token(test_users[0])
        res = self.client.post('/api/collections/',
                               data=json.dumps(test_collections[0]),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {token}'
                               )
        self.assertEquals(res.status_code, 201)
        result = json.loads(res.content)["data"]
        created_collection_id = result['id']
        res = self.client.get('/api/collections/' + str(created_collection_id) + '/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 200)

        res = self.client.delete('/api/collections/' + str(created_collection_id) + '/',
                                 content_type='application/json',
                                 HTTP_AUTHORIZATION=f'Bearer {token}'
                                 )
        self.assertEquals(res.status_code, 410)

        res = self.client.get('/api/collections/' + str(created_collection_id) + '/',
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 404)
