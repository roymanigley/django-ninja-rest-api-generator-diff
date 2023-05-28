import datetime

from django.test import Client
from django.test import TestCase
from pydantic.datetime_parse import timezone

from dummy_app.models import Gender
from dummy_app.tests_rest import helper

UPDATED_DESIGNATION = 'HR'


class GenderRestTest(TestCase):
    def setUp(self):
        self.token = helper.get_token()
        self.client = Client(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_all(self):
        # GIVEN
        self.create_persisted()
        # WHEN
        response = self.client.get('/api/gender')
        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["designation"], "IT")

    def test_get_all_should_return_empty_list(self):
        # WHEN
        response = self.client.get('/api/gender')
        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_by_id_existing(self):
        # GIVEN
        id = self.create_persisted().id
        # WHEN
        response = self.client.get(f'/api/gender/{id}')
        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["designation"], "IT")
        self.assertEqual(response.json()["id"], id)

    def test_get_by_id_non_existing(self):
        # GIVEN
        id = 999
        # WHEN
        response = self.client.get(f'/api/gender/{id}')
        # THEN
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Not Found")

    def test_post_valid(self):
        # GIVEN
        payload = self.create()
        # WHEN
        response = self.client.post('/api/gender', payload, content_type='application/json')
        # THEN
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get("designation"), "IT")
        id = response.json().get("id")
        self.assertIsNotNone(id)
        record = Gender.objects.filter(id=id).first()
        self.assertIsNotNone(record)
        self.assertEqual(record.designation, "IT")

    def test_post_invalid(self):
        # GIVEN
        payload = self.create()
        payload["designation"] = None
        # WHEN
        response = self.client.post('/api/gender', payload, content_type='application/json')
        # THEN
        self.assertEqual(response.status_code, 400)

    def test_put_with_existing_valid(self):
        # GIVEN
        id = self.create_persisted().id
        payload = self.create()
        payload["designation"] = UPDATED_DESIGNATION
        # WHEN
        response = self.client.put(f'/api/gender/{id}', payload, content_type='application/json')
        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("designation"), "HR")
        record = Gender.objects.filter(id=id).first()
        self.assertIsNotNone(record)
        self.assertEqual(record.designation, "HR")

    def test_put_existing_invalid(self):
        # GIVEN
        id = self.create_persisted().id
        payload = self.create()
        payload["designation"] = None
        # WHEN
        response = self.client.put(f'/api/gender/{id}', payload, content_type='application/json')
        # THEN
        self.assertEqual(response.status_code, 400)

    def test_put_non_existing(self):
        # GIVEN
        id = 999
        payload = self.create()
        # WHEN
        response = self.client.put(f'/api/gender/{id}', payload, content_type='application/json')
        # THEN
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(), '{"detail": "Not Found"}')








    def test_patch_existing_valid(self):
        # GIVEN
        id = self.create_persisted().id
        payload = self.create()
        payload["designation"] = UPDATED_DESIGNATION
        # WHEN
        response = self.client.patch(f'/api/gender/{id}', payload, content_type='application/json')
        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("designation"), "HR")
        record = Gender.objects.filter(id=id).first()
        self.assertIsNotNone(record)
        self.assertEqual(record.designation, "HR")

    def test_patch_existing_invalid(self):
        # GIVEN
        id = self.create_persisted().id
        payload = self.create()
        payload["designation"] = None
        # WHEN
        response = self.client.patch(f'/api/gender/{id}', payload, content_type='application/json')
        # THEN
        self.assertEqual(response.status_code, 500)

    def test_patch_non_existing(self):
        # GIVEN
        id = 999
        payload = self.create()
        # WHEN
        response = self.client.patch(f'/api/gender/{id}', payload, content_type='application/json')
        # THEN
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(), '{"detail": "Not Found"}')


# TODO: PATCH NULL id have nullable fields















    def test_delete_existing(self):
        # GIVEN
        id = self.create_persisted().id
        # WHEN
        response = self.client.delete(f'/api/gender/{id}')
        # THEN
        self.assertEqual(response.status_code, 203)
        record = Gender.objects.filter(id=id).first()
        self.assertIsNone(record)

    def test_delete_non_existing(self):
        # GIVEN
        id = 999
        # WHEN
        response = self.client.delete(f'/api/gender/{id}')
        # THEN
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(), '{"detail": "Not Found"}')

    @staticmethod
    def create_persisted(model: dict = None) -> Gender:
        if model is None:
            model = GenderRestTest.create()
        return Gender.objects.create(**model)

    @staticmethod
    def create():
        return {
            "designation": "IT",
            "modifier": "test",
            "modified_date": datetime.datetime.now(tz=timezone.utc).isoformat(),
            "creator": "test",
            "create_date": datetime.datetime.now(tz=timezone.utc).isoformat()
        }
