import psycopg2

url = "dbname='da43n1slakcjkc' user='msqgxzgmcskvst' host='ec2-54-80-184-43.compute-1.amazonaws.com' port=5432 password='9281f925b1e2298e8d62812d9d4e430c1054db62e918c282d7039fa85b1759fa'"

class database_setup(object):

    def __init__(self):
        self.conn = psycopg2.connect(url)
        self.cursor = self.conn.cursor()

    def destroy_tables(self):
        self.cursor.execute("""DROP TABLE IF EXISTS user CASCADE;""")

        self.conn.commit()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
            user_id SERIAL NOT NULL,
            fname VARCHAR(25) NOT NULL,
            lname VARCHAR(25) NOT NULL,
            post_date DATE NOT NULL DEFAULT CURRENT_DATE,
            phone TEXT  UNIQUE NOT NULL,
            password VARCHAR(256) NOT NULL,
            PRIMARY KEY (phone)
            );""")


        self.conn.commit()
