import requests
import time
import json
from tqdm import tqdm

class YaUploader:
    
    def __init__(self, yd_token: str):
        self.yd_token = yd_token

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
        
        for file_item in tqdm(url_dict):
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
            url_number += 1
            if response.status_code == 202:
                json_data.append({'file_name': file, 'size': file_type})               
                with open("file_info.json", 'w') as file:
                    json.dump(json_data, file, ensure_ascii=False, indent=2)
                    time.sleep(0.1) 
        print(f'Файлы успешно записаны')