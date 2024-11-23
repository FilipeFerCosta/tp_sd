from .base import *

# O IP privado é o da minha máquina, mude para o seu
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.0.0.214']

INSTALLED_APPS += [
    'whitenoise.runserver_nostatic',  # 
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
