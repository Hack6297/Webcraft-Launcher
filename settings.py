SECRET_KEY = 'fake-key'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = []
ROOT_URLCONF = 'urls'
MIDDLEWARE = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}