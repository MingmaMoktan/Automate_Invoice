"""
Django settings for the Invoice Automation SaaS project.
Refined Architecture: Base Configuration
"""

import os
import environ
from pathlib import Path

# ==============================================================================
# 1. PATHS & ENVIRONMENT INITIALIZATION
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Read the .env file from the project root
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# ==============================================================================
# 2. CORE SECURITY SETTINGS
# ==============================================================================
SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# ==============================================================================
# 3. APPLICATION DEFINITION
# ==============================================================================
INSTALLED_APPS = [
    # Django Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps (Add libraries like 'crispy_forms' here later)
    
    # Internal Project Apps
    'accounts.apps.AccountsConfig',
    'invoices.apps.InvoicesConfig',
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

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'


# ==============================================================================
# 4. TEMPLATE CONFIGURATION
# ==============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Global templates folder
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


# ==============================================================================
# 5. DATABASE CONFIGURATION
# ==============================================================================
DATABASES = {
    'default': env.db(),
}


# ==============================================================================
# 6. AUTHENTICATION & PASSWORD VALIDATION
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# (Optional) Tell Django to use a custom login URL later
# LOGIN_URL = 'login'
# LOGOUT_REDIRECT_URL = 'landing'


# ==============================================================================
# 7. INTERNATIONALIZATION
# ==============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# 8. STATIC & MEDIA FILES (The SaaS "Vault")
# ==============================================================================
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User-uploaded Invoice PDFs)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==============================================================================
# 9. MISCELLANEOUS
# ==============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# During development, emails are printed to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'