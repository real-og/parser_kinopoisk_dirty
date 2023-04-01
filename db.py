import psycopg2
import os


class Database(object):
    def __init__(self):
        self.conn = psycopg2.connect(
            database=str(os.environ.get('database')),
            user=str(os.environ.get('user')),
            password=str(os.environ.get('password')),
            host=str(os.environ.get('host')),
            port=str(os.environ.get('port'))
        )
        self.curs = self.conn.cursor()

    def __enter__(self):
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

def add_film(uuid, title, code, has_oscar, photo, year, country, director, actors, rating, genre, about):
    with Database() as curs:
        _SQL = f"""insert into robot_serial values
        ($${uuid}$$, $${title}$$, {code}, {has_oscar}, $${photo}$$, {year}, $${country}$$, $${director}$$, $${actors}$$, {rating}, $${genre}$$, $${about}$$);"""
        curs.execute(_SQL)
