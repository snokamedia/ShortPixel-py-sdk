
# ShortPixel Python SDK

## Overview
The ShortPixel Python SDK provides a simple and efficient way to optimize images using the ShortPixel API. It supports both URL-based and file-based image optimization, along with batch processing, folder optimization, and various configuration options.

## Features
- Optimize images by URL
- Optimize images by uploading local files
- Batch process images
- Resize images
- Keep or remove EXIF data
- Backup original images before optimization
- Detailed logging

## Installation
To use the ShortPixel Python SDK, you need to clone the repository from GitHub and install the required dependencies.

### Step 1: Clone the Repository
\`\`\`bash
git clone https://github.com/yourusername/shortpixel-python-sdk.git
\`\`\`

### Step 2: Navigate to the Project Directory
\`\`\`bash
cd shortpixel-python-sdk
\`\`\`

### Step 3: Install Dependencies
Ensure you have \`requests\` installed. You can install it using pip:
\`\`\`bash
pip install requests
\`\`\`

## Usage
Here’s how to use the ShortPixel Python SDK in your Python scripts.

### Step 1: Import the SDK
\`\`\`python
from shortpixel_sdk import ShortPixelSDK
\`\`\`

### Step 2: Initialize the SDK
Create an instance of the \`ShortPixelSDK\` class with your API key.
\`\`\`python
api_key = 'YOUR_API_KEY'
sdk = ShortPixelSDK(api_key)
\`\`\`

### Step 3: Optimize Images by URL
\`\`\`python
urls = ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']
result = sdk.batch_optimize_images(urls)
print(json.dumps(result, indent=2))
\`\`\`

### Step 4: Optimize Images by File
\`\`\`python
files = {'file1': '/path/to/image1.jpg', 'file2': '/path/to/image2.jpg'}
result = sdk.optimize_images_by_file(files)
print(json.dumps(result, indent=2))
\`\`\`

### Step 5: Optimize Entire Folder
Optimize all images in a folder, with optional resizing and EXIF data preservation.
\`\`\`python
folder_path = '/path/to/folder'
result = sdk.optimize_folder(folder_path, lossy=1, wait=30, resize=(800, 600), keep_exif=True, backup_folder='/path/to/backup')
print(json.dumps(result, indent=2))
\`\`\`

## Detailed Example
Here’s a full example script demonstrating the SDK usage:
\`\`\`python
import json
from shortpixel_sdk import ShortPixelSDK

# Initialize the SDK with your API key
api_key = 'YOUR_API_KEY'
sdk = ShortPixelSDK(api_key, log_level=logging.DEBUG)

# Optimize images by URL
urls = ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']
url_results = sdk.batch_optimize_images(urls)
print("URL Optimization Results:")
print(json.dumps(url_results, indent=2))

# Optimize images by file
files = {'file1': '/path/to/image1.jpg', 'file2': '/path/to/image2.jpg'}
file_results = sdk.optimize_images_by_file(files)
print("File Optimization Results:")
print(json.dumps(file_results, indent=2))

# Optimize entire folder with resizing and EXIF data preservation
folder_path = '/path/to/folder'
folder_results = sdk.optimize_folder(folder_path, lossy=1, wait=30, resize=(800, 600), keep_exif=True, backup_folder='/path/to/backup')
print("Folder Optimization Results:")
print(json.dumps(folder_results, indent=2))
\`\`\`

## Logging
The SDK uses Python's logging module for detailed information during optimization. The logging level can be adjusted when initializing the SDK.

\`\`\`python
import logging
sdk = ShortPixelSDK(api_key, log_level=logging.DEBUG)
\`\`\`

## Conclusion
The ShortPixel Python SDK simplifies the process of image optimization using ShortPixel's powerful API. With support for both URL-based and file-based optimization, batch processing, and various configuration options, it provides a flexible and robust solution for all your image optimization needs.
