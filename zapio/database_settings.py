from .creds import database_creds


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': database_creds["name"],
        'USER': database_creds["user"],
        'CONN_MAX_AGE' : database_creds["CONN_MAX_AGE"],
        'PASSWORD': database_creds["PASSWORD"],
        'HOST': database_creds["HOST"],
        'PORT': database_creds["Port"],
    }
}