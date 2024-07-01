import requests
import json
import os
import time
import logging
import shutil

class ShortPixelSDK:
    def __init__(self, api_key, plugin_version='MYSDK', log_level=logging.INFO):
        self.api_key = api_key
        self.plugin_version = plugin_version
        self.reducer_url = 'https://api.shortpixel.com/v2/reducer.php'
        self.post_reducer_url = 'https://api.shortpixel.com/v2/post-reducer.php'
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)

    def optimize_images_by_url(self, url_list, replace_original=False, lossy=1, wait=20, resize=0, resize_width=1024, resize_height=1024, cmyk2rgb=1, keep_exif=0, convertto=None, bg_remove=None, refresh=0, paramlist=None, returndatalist=None, **kwargs):
        payload = {
            'key': self.api_key,
            'plugin_version': self.plugin_version,
            'lossy': lossy,
            'wait': wait,
            'resize': resize,
            'resize_width': resize_width,
            'resize_height': resize_height,
            'cmyk2rgb': cmyk2rgb,
            'keep_exif': keep_exif,
            'convertto': convertto,
            'bg_remove': bg_remove,
            'refresh': refresh,
            'urllist': url_list,
            'paramlist': paramlist,
            'returndatalist': returndatalist,
            **kwargs
        }
        response = requests.post(self.reducer_url, data=json.dumps(payload))
        result = response.json()
        if replace_original:
            self.replace_original_files(result)
        return result

    def optimize_images_by_file(self, file_paths, replace_original=False, lossy=1, wait=30, resize=0, resize_width=1024, resize_height=1024, cmyk2rgb=1, keep_exif=0, convertto=None, bg_remove=None, refresh=0, paramlist=None, returndatalist=None, **kwargs):
        files = {name: open(path, 'rb') for name, path in file_paths.items()}
        payload = {
            'key': self.api_key,
            'plugin_version': self.plugin_version,
            'lossy': lossy,
            'wait': wait,
            'resize': resize,
            'resize_width': resize_width,
            'resize_height': resize_height,
            'cmyk2rgb': cmyk2rgb,
            'keep_exif': keep_exif,
            'convertto': convertto,
            'bg_remove': bg_remove,
            'refresh': refresh,
            'file_paths': json.dumps(file_paths),
            'paramlist': paramlist,
            'returndatalist': returndatalist,
            **kwargs
        }
        response = requests.post(self.post_reducer_url, files=files, data=payload)
        for file in files.values():
            file.close()
        result = response.json()
        if replace_original:
            self.replace_original_files(result, local_file_paths=file_paths)
        return result

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

    def batch_optimize_images(self, url_list, replace_original=False, lossy=1, wait=20, **kwargs):
        results = []
        for url in url_list:
            result = self.optimize_images_by_url([url], replace_original=replace_original, lossy=lossy, wait=wait, **kwargs)
            if result[0]['Status']['Code'] == 1:
                for _ in range(wait):
                    time.sleep(1)
                    result = self.check_image_status(url, lossy=lossy, wait=wait)
                    if result[0]['Status']['Code'] == 2:
                        break
            results.append(result)
        return results

    def optimize_folder(self, folder_path, replace_original=False, lossy=1, wait=30, resize=None, keep_exif=False, backup_folder=None, **kwargs):
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
        result = self.optimize_images_by_file(files, replace_original=replace_original, **payload)
        return result

    def replace_original_files(self, results, local_file_paths=None):
        for result in results:
            if result['Status']['Code'] == "2":
                optimized_url = result.get('LossyURL') or result.get('LosslessURL')
                if optimized_url:
                    file_key = result.get('Key')
                    if local_file_paths and file_key in local_file_paths:
                        local_path = local_file_paths[file_key]
                        optimized_image = requests.get(optimized_url).content
                        with open(local_path, 'wb') as f:
                            f.write(optimized_image)
                            self.logger.info(f"Replaced original file with optimized file: {local_path}")

    def backup_files(self, files, backup_folder):
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
        for file_key, file_path in files.items():
            backup_path = os.path.join(backup_folder, os.path.basename(file_path))
            shutil.copy2(file_path, backup_path)
            self.logger.info(f"Backed up {file_path} to {backup_path}")
