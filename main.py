from api.vk_api import VK
from api.yandex import YaUploader

if __name__ == '__main__':
    yd_token = input('Введите токен Яндекс.Диска: ')
    vk_id = input('Введите VK ID: ')  # VK ID: 552934290
    photo_quantity = input('Введите количество загружаемых файлов: ')
    response = VK(vk_id, 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd')
    url_dict = response.get_photo(photo_quantity)
    file_path = str(vk_id)
    uploader = YaUploader(yd_token)
    uploader.create_ya_folder(file_path)
    uploader.upload(url_dict)