import requests
import time
import json

class VK:
    
    def __init__(self, vk_id, vk_token):
        self.vk_id = vk_id
        self.vk_token = vk_token
    
    def get_photo(self, photo_quantity, album_id='profile'):
        url = 'https://api.vk.com/method/photos.get'
        param = {'extended': 'likes',
                 'album_id': album_id,
                 'user_ids': self.vk_id,
                 'access_token': self.vk_token,
                 'v': '5.131'
                 }
        response = requests.get(url, params=param)
        items = response.json().get('response').get('items')
        photo_data = []
        photo_number = 0
        for item in items:
            sizes = item.get('sizes')
            max_size = 0
            index = 0
            for size in sizes:
                current_size = size.get('height') * size.get('width')
                if current_size > max_size:
                    max_size = current_size
                    index = sizes.index(size)
                if max_size == 0:
                    index = -1
            date = item.get('date')
            type = sizes[index].get('type')
            url = sizes[index].get('url')
            likes = item.get('likes').get('count')
            photo_data.append({'file_name': likes, 'file_url': url, 'type': type, 'date': date})
            photo_number += 1
            if photo_number == photo_quantity:
                break
        return photo_data

class YaUploader:
    
    def __init__(self, yd_token: str):
        self.yd_token = yd_token

    def create_json(self, json_data):
        with open("file_info.json", 'w') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)

    def create_ya_folder(self, file_path):
        self.file_path = file_path
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Authorization': 'OAuth {}'.format(self.yd_token)
        }
        params = {
            'path': self.file_path
        }
        response = requests.put(url, headers=headers, params=params)
        if response.status_code == 201:
            print(f'Папка {self.file_path} создана')
        elif response.status_code == 409:
            print(f'Папка {self.file_path} уже была создана')
        else:
            print('Ошибка', response)

    def upload(self, url_dict):
        
        file_list = []
        json_data = []
        url_number = 0
        
        for file_item in url_dict:
            file = str(file_item.get('file_name'))
            file_url = file_item.get('file_url')
            file_date = file_item.get('date')
            file_type = file_item.get('type')
            if file in file_list:
                file = str(file) + str(time.strftime('_%d.%m.%y', time.gmtime(file_date)))
            else:
                file_list.append(file)
            headers = {'Accept': 'application/json',
                       'Authorization': 'OAuth {}'.format(self.yd_token)}
            params = {'path': self.file_path + '/' + file,
                      'url': file_url}
            url = 'https://cloud-api.yandex.net/post/v1/disk/resources/upload'
            response = requests.post(url, headers=headers, params=params)
            quantity_url = len(url_dict)
            url_number += 1
            if response.status_code == 202:
                json_data.append({'file_name': file, 'size': file_type})
                print(f'Файл успешно записан {url_number}/{quantity_url}')
            else:
                print(f'Ошибка {url_number}/{quantity_url}')
        uploader.create_json(json_data)

if __name__ == '__main__':
    yd_token = input('Введите токен Яндекс.Диска: ')
    vk_id = input('Введите VK ID: ')  # VK ID: 552934290
    photo_quantity = input('Введите количество загружаемых файлов: ')
    response = VK(vk_id, 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd')
    url_dict = response.get_photo(photo_quantity)
    print(url_dict)
    file_path = str(vk_id)
    uploader = YaUploader(yd_token)
    uploader.create_ya_folder(file_path)
    uploader.upload(url_dict)