import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.staticfiles.storage import FileSystemStorage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / 'data/web'

load_dotenv(BASE_DIR / 'dotenv_files/env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') 

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'accounts',
    'django.contrib.auth',
    'jazzmin',
    'django.contrib.admin',
    'adminsortable2',  # Admin Sortable 2
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_select2',
    # Third-party apps
    # Your apps
    'form',  # Your forms app
    'cars',  # Your cars app
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE')

TIME_ZONE = os.getenv('TIME_ZONE')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = DATA_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = DATA_DIR / 'media'

# Custom static files storage to ignore .scss and sass directories
class CustomStaticFilesStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if name.endswith(".scss") or 'sass' in name:
            return None  # Ignora arquivos SCSS e diretórios sass
        return super().get_available_name(name, max_length=max_length)

# Atualize para o nome correto do seu projeto
STATICFILES_STORAGE = 'project.settings.CustomStaticFilesStorage'


# Email settings
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django Jazzmin Configuration
JAZZMIN_SETTINGS = {
    "site_title": "Administração do Projeto",
    "site_header": "Administração",
    "site_brand": "Lucas Multimarcas",
    "site_logo": "base/img/racing-car.png",
    "welcome_sign": "Bem-vindo ao painel de administração",
    "copyright": "Lucas Multimarcas",
    "copyright": "Lucas Dev",
    "hide_recent_actions": True,
    "theme": "spacelab",
    "dark_mode_theme": "darkly",
    "search_model": ["cars.Car",],

    # Ícones para os modelos
    "icons": {
        "form.Pessoa": "fa-solid fa-person",
        "form.Indicacao": "fas fa-search",
        "cars.Car": "fa-solid fa-car-rear",
        "cars.Brand": "fa-solid fa-copyright",
        "cars.Model": "fa-solid fa-boxes-stacked",
        "accounts.CustomUser": "fa-solid fa-user",
        "accounts.UserProfile" : "fa-solid fa-address-card",
        "auth.group" : "fa-solid fa-people-group",
    },

    # Configurar a ordem das apps no menu lateral
    "order_with_respect_to": ["cars", "form"],
}

# --- Login Logout User --- # 
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'cars:home'
LOGOUT_REDIRECT_URL = 'login'


# settings.py
SESSION_COOKIE_AGE = 1209600  # Tempo padrão de expiração do cookie (2 semanas)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Define se a sessão expira ao fechar o navegador

AUTH_USER_MODEL = 'accounts.CustomUser'


