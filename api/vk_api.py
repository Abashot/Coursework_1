import requests

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