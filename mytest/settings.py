import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасное получение SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-default-key-change-in-production')

# DEBUG из переменных окружения
DEBUG = True #os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = [
    '176.96.241.174', 
    'buxorobilimdonlarmaktabi.uz',
    'www.buxorobilimdonlarmaktabi.uz',
    'localhost',
    '127.0.0.1'
]

# Приложения
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'accounts',
    'tests_app',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mytest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mytest.wsgi.application'

#PostgreSQL
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # } 
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'buxoro_db',
        'USER': 'buxoro_user',
        'PASSWORD': 'Bahriddin0121',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Валидаторы паролей
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

# Интернационализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки безопасности для production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# CORS настройки
CORS_ALLOWED_ORIGINS = [
    "https://buxorobilimdonlarmaktabi.uz",
    "https://www.buxorobilimdonlarmaktabi.uz",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Кастомная модель пользователя
AUTH_USER_MODEL = 'accounts.User'

# WhiteNoise для статических файлов (уже настроен выше)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# В settings.py проверьте эти пути:
BASE_DIR = Path(__file__).resolve().parent.parent  # Должно указывать на /home/baxadev/my_test

# Убедитесь что эти пути существуют
# print("BASE_DIR:", BASE_DIR)
# print("Static dirs:", BASE_DIR / 'static')

# Jazzmin Settings
JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "Buxoro Bilimdonlar Maktabi",

    # Title on the brand, and the login screen
    "site_header": "Buxoro Bilimdonlar",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "books.ico",

    # Welcome text on the login screen
    "welcome_sign": "Buxoro Bilimdonlar Maktabi Admin Paneliga Xush Kelibsiz",

    # Copyright on the footer
    "copyright": "Buxoro Bilimdonlar Maktabi",

    # Field name on user model that contains avatar image
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Bosh Sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Saytga O'tish", "url": "/", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "tests_app"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right
    "usermenu_links": [
        {"name": "Saytga O'tish", "url": "/", "new_window": True},
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu
    "hide_apps": [],

    # Hide these models when generating side menu
    "hide_models": [],

    # List of apps to base side menu ordering off of
    "order_with_respect_to": ["accounts", "tests_app"],

    # Custom icons for side menu apps
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.User": "fas fa-user",
        "tests_app.Test": "fas fa-file-alt",
        "tests_app.Question": "fas fa-question-circle",
        "tests_app.Answer": "fas fa-check-circle",
    },

    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
}

# Jazzmin UI Configuration
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
}
