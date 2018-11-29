import base64
import os
import tempfile

from django.conf import settings
from django.test.utils import override_settings
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from file_service.files import models as file_models
from file_service.files.models import FileExtension, FileType
from trood_auth_client.authentication import TroodUser

aac_file_data = "//FQgCi//N4CAExhdmM1Ny44OS4xMDAAQjYf///8MACPslW0kC0TE0TC0LBc31HLWWcVF1U1lqfcrWhzJUSt2Otf//IYZnBrSL7MwvbLX0D7XXMXU/6889ow33jjGYuyV8DO0nBtk9c2PnoELJsgeAkY+fYUb+W+Z2VJm7GwZsGZhuwRMN0iJhmwHYDmI+cr8AnEr5QZEm6ZunYlff0lYLcP84ORJpErmITIWXe1mLinxBzo8CzywwCxMuhLgGBsByI+0lnLYppx5jYceouxDYbOAgIXKMkQZ7BUJYUFB6Jafrl479u6gJcuzSty3MCwEZ2zgU8py5GS5ZkWWZZ2pAz9kud1731ZZRAQFkmzPLsuOyqfMJZ8z8fnTLHjrSCLReHQ+LReLQ+FzfUctZZxUXVTWWp9ytaDDQ2AAAAAAAAAAAAAcP/xUIAqf/whGw////2NAEdYqvoaFo4FoYDooHo6C741Rz045vjLzVFpT8uEmRVUnneQP3Ow9Z7R/vKzf+V48TzVvGcz89SbrruJvu4+kge3N1C+Viqn6rvOF+9+9+B46+Q0jicTx20j8DjTPHazkaVLGsWuc1muvsDlM7GmVIs7OqWMbI2EXI5TicTOxrztMK82HI1mu41Nf8dynjtZrthyONYzuRxuY//uUWoA0la2WNyONambK+0ONyPWazZbDibDGqWM7O7Wbwdy8/sYv5fuho8Hiw4oQ3NqOpZqamaiyuizRZCEkNGaFGa7S7klkJKM0NSSdkhPFcSKi8iaS8jUzQ5N4ZoaklGpqZpqM1mpJcFGpMdGuvuRpG9xKMvOUqZ2djZHExw50Ii0Yi0Ih0Xi0nhd8ao56cc3xl5qi0p+XCTIqjWt4AAAAAAAAAAAAAAADg=="
jpg_file_data = "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigD//2Q=="

def create_temp_file(ext='.txt', data=None):
    _, filename = tempfile.mkstemp(ext)
    if data:
        tmp_file = open(filename, 'wb')
        tmp_file.write(base64.b64decode(data))
    else:
        tmp_file = open(filename, 'w')
        tmp_file.write("Test sentence")

    tmp_file.close()
    tmp_file = open(filename, 'rb')
    return tmp_file, filename


class FilesBehaviourTestCase(APITestCase):

    def setUp(cls):
        cls.client = APIClient()

        trood_user = TroodUser({
            "id": 1,
        })

        cls.client.force_authenticate(user=trood_user)
        FileExtension.objects.create(extension='jpg')
        FileExtension.objects.create(extension='aac')

        FileType.objects.get_or_create(id="IMAGE", mime="image/jpeg")
        FileType.objects.get_or_create(id="AUDIO", mime="audio/x-hx-aac-adts")

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_can_upload_image_file(self):
        url = reverse('api:file-list', )
        test_file, test_file_path = create_temp_file('.jpg', data=jpg_file_data)
        file_data = {'file': test_file, 'name': 'myfile'}
        response = self.client.post(url, data=file_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:file-detail', kwargs={'pk': response.data['id']})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['size'], os.path.getsize(test_file_path))
        self.assertEqual(response.data['mimetype'], 'image/jpeg')
        self.assertEqual(response.data['type'], 'IMAGE')
        self.assertContains(response, '{}{}'.format(settings.FILES_BASE_URL, response.data['id']))

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_can_upload_audio_file(self):
        url = reverse('api:file-list', )
        test_file, test_file_path = create_temp_file('.aac', data=aac_file_data)
        file_data = {'file': test_file, 'name': 'myfile'}
        response = self.client.post(url, data=file_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:file-detail', kwargs={'pk': response.data['id']})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], 'AUDIO')
        self.assertEqual(response.data['mimetype'], 'audio/x-hx-aac-adts')

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_cant_upload_incompatible_type(self):
        url = reverse('api:file-list', )
        file_data = {'file': create_temp_file('.exe'), 'name': 'myfile'}
        response = self.client.post(url, data=file_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_update_audio_file_metadata(self):
        url = reverse('api:file-list', )
        file_data = {'file': create_temp_file('.aac', data=aac_file_data), 'name': 'myfile'}
        response = self.client.post(url, data=file_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:file-detail', kwargs={'pk': response.data['id']})
        meta_data = {
            'mp3': create_temp_file('.mp3'),
            'length': 3123,
            'ready': True
        }
        response = self.client.patch(url + 'metadata/', data=meta_data, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ready'], True)

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_update_image_file_metadata(self):
        url = reverse('api:file-list', )
        file_data = {'file': create_temp_file('.jpg', data=jpg_file_data), 'name': 'myfile'}
        response = self.client.post(url, data=file_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:file-detail', kwargs={'pk': response.data['id']})
        meta_data = {
            'small': create_temp_file('.jpg'),
            'medium': create_temp_file('.jpg'),
            'large': create_temp_file('.jpg'),
            'xlarge': create_temp_file('.jpg'),
            'ready': True
        }
        response = self.client.patch(url + 'metadata/', data=meta_data, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['ready'], True)
        self.assertContains(response, '{}_small.jpg'.format(response.data['id']))
        self.assertContains(response, '{}_medium.jpg'.format(response.data['id']))
        self.assertContains(response, '{}_large.jpg'.format(response.data['id']))
        self.assertContains(response, '{}_xlarge.jpg'.format(response.data['id']))

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_update_audio_file_metadata_with_error_message(self):
        url = reverse('api:file-list', )
        file_data = {'file': create_temp_file('.aac', data=aac_file_data), 'name': 'myfile'}
        response = self.client.post(url, data=file_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('api:file-detail', kwargs={'pk': response.data['id']})
        meta_data = {
            'message':  'Error something goes wrong',
            'ready': False
        }
        response = self.client.patch(url + 'metadata/', data=meta_data, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ready'], False)
        self.assertEqual(response.data['metadata']['message'], 'Error something goes wrong')


class FileExtensionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        trood_user = TroodUser({
            "id": 1,
        })

        self.client.force_authenticate(user=trood_user)


    def test_create_extension(self):
        data = {
            'extension': 'jpg'
        }
        response = self.client.post('/api/v1.0/extensions/',
                                    data=data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['extension'] == 'jpg'

    def test_create_empty_extension_fail(self):
        data = {
            'extension': ''
        }
        response = self.client.post('/api/v1.0/extensions/',
                                    data=data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_extension_lowercase(self):
        data = {
            'extension': 'JPG'
        }
        response = self.client.post('/api/v1.0/extensions/',
                                    data=data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
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

        assert response.status_code == status.HTTP_200_OK
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

        assert response.status_code == status.HTTP_200_OK
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

        assert response.status_code == status.HTTP_200_OK
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
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = self.client.get('/api/v1.0/extensions/',
                                   format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['extension'] == 'mp4'