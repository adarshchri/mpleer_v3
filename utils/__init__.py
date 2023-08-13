import requests


def download_file(url):
    photo = requests.get(url)
    return photo.content
