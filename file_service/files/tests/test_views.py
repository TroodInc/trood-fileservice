from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, \
    HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase, APIClient


class FileExtensionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_extension(self):
        data = {
            'extension': 'jpg'
        }
        response = self.client.post('/api/v1.0/extensions/',
                                    data=data, format='json')

        assert response.status_code == HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['extension'] == 'jpg'

    def test_create_empty_extension_fail(self):
        data = {
            'extension': ''
        }
        response = self.client.post('/api/v1.0/extensions/',
                                    data=data, format='json')

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_create_extension_lowercase(self):
        data = {
            'extension': 'JPG'
        }
        response = self.client.post('/api/v1.0/extensions/',
                                    data=data, format='json')

        assert response.status_code == HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['extension'] == 'jpg'

    def test_get_extension(self):
        data = {
            'extension': 'jpg'
        }
        response = self.client.post('/api/v1.0/extensions/',
                                    data=data, format='json')

        ext_id = response.data['id']
        response = self.client.get(f'/api/v1.0/extensions/{ext_id}/',
                                   format='json')

        assert response.status_code == HTTP_200_OK
        assert response.data['id'] == ext_id
        assert response.data['extension'] == 'jpg'

    def test_modify_extension_lowercase(self):
        data = {
            'extension': 'jpg'
        }
        response = self.client.post('/api/v1.0/extensions/',
                                    data=data, format='json')

        ext_id = response.data['id']

        modify_data = {
            'extension': 'MP4'
        }
        response = self.client.put(f'/api/v1.0/extensions/{ext_id}/',
                                   data=modify_data, format='json')

        assert response.status_code == HTTP_200_OK
        assert response.data['id'] == ext_id
        assert response.data['extension'] == 'mp4'

    def test_list_extensions(self):
        data = {
            'extension': 'jpg'
        }
        self.client.post('/api/v1.0/extensions/', data=data, format='json')

        data = {
            'extension': 'mp4'
        }
        self.client.post('/api/v1.0/extensions/', data=data, format='json')

        response = self.client.get('/api/v1.0/extensions/', format='json')

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 2

    def test_delete_extension(self):
        data = {
            'extension': 'jpg'
        }
        response = self.client.post('/api/v1.0/extensions/',
                                    data=data, format='json')
        ext_id = response.data['id']

        data = {
            'extension': 'mp4'
        }
        self.client.post('/api/v1.0/extensions/',
                         data=data, format='json')

        response = self.client.delete(f'/api/v1.0/extensions/{ext_id}/',
                                      format='json')
        assert response.status_code == HTTP_204_NO_CONTENT

        response = self.client.get('/api/v1.0/extensions/',
                                   format='json')

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['extension'] == 'mp4'