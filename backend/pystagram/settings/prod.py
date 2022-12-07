from pystagram.settings.common import *

SECRET_KEY = config("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
    "pystagram.com",
    "www.pystagram.com",
]
