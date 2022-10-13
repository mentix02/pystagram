import requests


def send_create_req():
    data = {'caption': "Hello world"}
    r = requests.post('http://127.0.0.1:8000/api/v1/post/create/')
