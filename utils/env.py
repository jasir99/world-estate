import os

def get_env(argument):
    if argument == 'SECRET_KEY':
        SECRET_KEY = os.environ.get(argument)
        if SECRET_KEY is None:
            return '0w%a+_@9km^)+i4*w*$mt!lgkf$u32$&jtm#udtxnt_!6xvgud'
        return SECRET_KEY


    elif argument == 'DATABASE_USER':
        DB_USER = os.environ.get(argument)
        if DB_USER is None:
            return 'postgres'
        return DB_USER

    elif argument == 'DATABASE_PASSWORD':
        DB_PASSWORD = os.environ.get(argument)
        if DB_PASSWORD is None:
            return 'astrit'
        return DB_PASSWORD

    elif argument == 'DATABASE':
        DATABASE = os.environ.get(argument)
        if DATABASE is None:
            return 'test-app'
        return DATABASE



