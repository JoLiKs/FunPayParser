import psycopg2

DBNAME = 'postgres'
USER = 'postgres'
PASSWORD = '56317'
HOST = '127.0.0.1'


def create_flats_table():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS flats(
                id serial PRIMARY KEY,
                link CHARACTER VARYING(300) UNIQUE NOT NULL,
                reference CHARACTER VARYING(30),
                price INTEGER,
                title CHARACTER VARYING(1000),
                description CHARACTER VARYING(3000),
                date TIMESTAMP WITH TIME ZONE
                )''')


def insert_flat(flat):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO flats (link, reference, price, title, description, date) VALUES (%s, %s, %s, %s, %s, %s) 
                ON CONFLICT (link) DO UPDATE 
                SET 
                link = EXCLUDED.link, 
                price = EXCLUDED.price, 
                title = EXCLUDED.title, 
                description = EXCLUDED.description, 
                date = EXCLUDED.date
                 ''',
                        (flat.link, flat.reference, flat.price, flat.title, flat.description, flat.date)
                        )

def create_lots_table():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS lots(
                id serial PRIMARY KEY,
                link CHARACTER VARYING(300) UNIQUE NOT NULL,
                reference CHARACTER VARYING(30),
                price FLOAT,
                title CHARACTER VARYING(1000),
                seller_rep INTEGER
                )''')


def insert_lot(lot):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO lots (link, reference, price, title, seller_rep) VALUES (%s, %s, %s, %s, %s) 
                ON CONFLICT (link) DO UPDATE 
                SET 
                link = EXCLUDED.link,
                reference = EXCLUDED.reference, 
                price = EXCLUDED.price, 
                title = EXCLUDED.title, 
                seller_rep = EXCLUDED.seller_rep
                 ''',
                        (lot.link, lot.reference, lot.price, lot.title, lot.seller_rep)
                        )