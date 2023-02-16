NIPTViewer is developed using django and most changes to the server can be made by modifying [niptviewer/settings.py](https://github.com/clinical-genomics-uppsala/NIPTViewer/blob/dev/niptviewer/niptviewer/settings.py), for more information please visist [django homepage](https://docs.djangoproject.com/en/3.2/ref/settings/).

Some of NIPTViewer settings that can and should modified before running NIPTViewer in ant kind of production environment, by simply setting environment variables.

# ENV config

## SECRET_KEY
`SECRET_KEY`: key is used to provide cryptographic signing. This key is mostly used to sign session cookies.

## Time selection
Default time span can be set for the different parts of NIPTviewer

### Web page
`DEFAULT_TIME_SELECTION`: number of month from today that should be shown, default 9999 -> show all data

### Sample Report
`DEFAULT_TIME_SELECTION_SAMPLE_REPORT`: number of month from today that should be shown in pdf report, default 24

### QC Report
`DEFAULT_TIME_SELECTION_QC_REPORT`: number of month from today that should be shown in pdf report, default 12

## Database 

Default setting file currenlty support 3 types of databases, sqlite3, postgres and mssql

Settable variables are:

- DATABASE
- ENGINE
- NAME
- USER
- PASSWORD
- HOST
- PORT

database section from the setting file
```python
if os.environ.get('DATABASE', "sqlite3") == "sqlite3":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
elif os.environ.get('DATABASE', "sqlite3") == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
            "USER": os.environ.get("SQL_USER", "user"),
            "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
            "HOST": os.environ.get("SQL_HOST", "localhost"),
            "PORT": os.environ.get("SQL_PORT", "5432"),
        }
    }
elif os.environ.get('DATABASE', "sqlite3") == "mssql":
    DATABASES = {
        "default": {
            "ENGINE": 'mssql',
            "NAME": get_secrets('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
            "USER": get_secrets('SQL_USER', 'user'),
            "PASSWORD": get_secrets('SQL_PASSWORD', 'password'),
            "HOST": os.environ.get('SQL_HOST', 'localhost'),
            "PORT": os.environ.get('SQL_PORT', ''),
            "OPTIONS": {
                'driver': 'ODBC Driver 17 for SQL Server',
                'host_is_server': True,
                'connection_timeout': 30,
                'collation': 'SQL_Latin1_General_CP1_CI_AS',
                'extra_params': 'TrustServerCertificate=yes;Encrypt=yes',
            }
        }
    }
```

Support for more database can be added by modifying this section of settings.py

