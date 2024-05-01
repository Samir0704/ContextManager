import psycopg2

db_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '123',
    'port': 5432
}

class DbConnect:
    def __init__(self, db_params):
        self.db_params = db_params
        self.conn = psycopg2.connect(**self.db_params)

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class Person:
    def __init__(self,
                 id: int | None = None,
                 full_name: str | None = None,
                 age: int | None = None,
                 email: str | None = None,):
        self.id = id
        self.full_name = full_name,
        self.age = age,
        self.email = email


    def get_one(self):
        with DbConnect(db_params) as cur:
            select_query = 'select * from Person;'
            cur.execute(select_query)
            person: list[Person] = []
            for row in cur.fetchone():
                person.append(Person(id=row[0], full_name=row[1], age=row[2], email=row[3]))
            return person

    def save(self):
        with DbConnect(db_params) as cur:
            insert_query = 'insert into Person (id,full_name,age,email) values (%s,%s,%s,%s);'
            insert_params = (self.id, self.full_name, self.age, self.email)
            cur.execute(insert_query, insert_params)
            print('INSERT 0 1')

    def __repr__(self):
        return f'Person({self.id} => {self.full_name} => {self.age} => {self.email})'

person = Person(id=1, full_name='Samir', age=20, email='samir@gmail.com')
person.save()

