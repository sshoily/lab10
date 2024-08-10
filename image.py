import requests
import ctypes
from PIL import Image
from io import BytesIO

# Constants
IMAGE_URL = 'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg'
IMAGE_PATH = r'C:\temp\kitty.jpg'
MAX_SIZE = (800, 600)

def main():
    image_data = download_image(IMAGE_URL)
    if image_data:
        image_data = resize_image(image_data, MAX_SIZE)
        if save_image_file(image_data, IMAGE_PATH):
            set_desktop_background_image(IMAGE_PATH)
    else:
        print("Image download failed.")
    return

def download_image(image_url):
    """Downloads an image from a specified URL.

    Args:
        image_url (str): URL of image

    Returns:
        bytes: Binary image data, if successful. None, if unsuccessful.
    """
    print(f'Downloading image from {image_url}...', end='')
    try:
        resp_msg = requests.get(image_url)
        resp_msg.raise_for_status()
        print('success')
        return resp_msg.content
    except requests.RequestException as e:
        print(f'failure: {e}')
        return None

def resize_image(image_data, max_size):
    """Resizes the image to the specified maximum size while maintaining aspect ratio.

    Args:
        image_data (bytes): Binary image data
        max_size (tuple[int, int]): Maximum image size in pixels (width, height)

    Returns:
        bytes: Resized binary image data
    """
    with Image.open(BytesIO(image_data)) as img:
        img.thumbnail(max_size)
        with BytesIO() as output:
            img.save(output, format=img.format)
            return output.getvalue()

def save_image_file(image_data, image_path):
    """Saves image data as a file on disk.

    Args:
        image_data (bytes): Binary image data
        image_path (str): Path to save image file

    Returns:
        bool: True, if successful. False, if unsuccessful
    """
    try:
        print(f"Saving image file as {image_path}...", end='')
        with open(image_path, 'wb') as file:
            file.write(image_data)
        print("success")
        return True
    except Exception as e:
        print(f"failure: {e}")
        return False

def set_desktop_background_image(image_path):
    """Sets the desktop background image to a specific image.

    Args:
        image_path (str): Path of image file

    Returns:
        bool: True, if successful. False, if unsuccessful
    """
    print(f"Setting desktop to {image_path}...", end='')
    SPI_SETDESKWALLPAPER = 20
    try:
        if ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3):
            print("success")
            return True
        else:
            print("failure")
            return False
    except Exception as e:
        print(f"failure: {e}")
        return False

if __name__ == '__main__':
    main()
