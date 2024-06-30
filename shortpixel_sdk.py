import requests
import json
import os
import time
import logging

class ShortPixelSDK:
    def __init__(self, api_key, plugin_version='MYSDK', log_level=logging.INFO):
        self.api_key = api_key
        self.plugin_version = plugin_version
        self.reducer_url = 'https://api.shortpixel.com/v2/reducer.php'
        self.post_reducer_url = 'https://api.shortpixel.com/v2/post-reducer.php'
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)

    def optimize_images_by_url(self, url_list, lossy=1, wait=20, **kwargs):
        payload = {
            'key': self.api_key,
            'plugin_version': self.plugin_version,
            'lossy': lossy,
            'wait': wait,
            'urllist': url_list,
            **kwargs
        }
        response = requests.post(self.reducer_url, data=json.dumps(payload))
        return response.json()

    def optimize_images_by_file(self, file_paths, lossy=1, wait=30, **kwargs):
        files = {name: open(path, 'rb') for name, path in file_paths.items()}
        payload = {
            'key': self.api_key,
            'plugin_version': self.plugin_version,
            'lossy': lossy,
            'wait': wait,
            'file_paths': json.dumps(file_paths),
            **kwargs
        }
        response = requests.post(self.post_reducer_url, files=files, data=payload)
        for file in files.values():
            file.close()
        return response.json()

    def check_image_status(self, url, lossy=1, wait=20):
        payload = {
            'key': self.api_key,
            'plugin_version': self.plugin_version,
            'lossy': lossy,
            'wait': wait,
            'urllist': [url]
        }
        response = requests.post(self.reducer_url, data=json.dumps(payload))
        return response.json()

    def batch_optimize_images(self, url_list, lossy=1, wait=20, **kwargs):
        results = []
        for url in url_list:
            result = self.optimize_images_by_url([url], lossy=lossy, wait=wait, **kwargs)
            if result[0]['Status']['Code'] == 1:
                for _ in range(wait):
                    time.sleep(1)
                    result = self.check_image_status(url, lossy=lossy, wait=wait)
                    if result[0]['Status']['Code'] == 2:
                        break
            results.append(result)
        return results

    def optimize_folder(self, folder_path, lossy=1, wait=30, resize=None, keep_exif=False, backup_folder=None, **kwargs):
        files = {f"file{index}": os.path.join(folder_path, file) for index, file in enumerate(os.listdir(folder_path))}
        if backup_folder:
            self.backup_files(files, backup_folder)
        payload = {
            'key': self.api_key,
            'plugin_version': self.plugin_version,
            'lossy': lossy,
            'wait': wait,
            'keep_exif': 1 if keep_exif else 0,
            **kwargs
        }
        if resize:
            payload.update({'resize': 1, 'resize_width': resize[0], 'resize_height': resize[1]})
        response = self.optimize_images_by_file(files, **payload)
        return response

    def backup_files(self, files, backup_folder):
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
        for file_key, file_path in files.items():
            backup_path = os.path.join(backup_folder, os.path.basename(file_path))
            os.rename(file_path, backup_path)
            self.logger.info(f"Backed up {file_path} to {backup_path}")
