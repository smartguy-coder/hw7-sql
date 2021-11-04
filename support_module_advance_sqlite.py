import sqlite3 as sq
from random import choice, randint
from catalog import NAMES_SET, SURNAMES_SET, AGE_INTERVAL


name_of_db = 'advance_database.db'

# done
def create_table_professions():
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS professions (
                    id INTEGER primary key AUTOINCREMENT,
                    profession TEXT not null UNIQUE);''')
        print("Table professions was created")
        connection.commit()
        cursor.close()

# done
def add_new_profession(new_profession: str = None):
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        if new_profession:
            cursor.execute(f"""INSERT OR IGNORE INTO professions (profession) VALUES (?);""", (new_profession, ))
            print("Data into table professions was added")
        else:
            print(f'you have entered no parameters')
        connection.commit()
        cursor.close()

# done
def create_table_genders():
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS genders (
                    id INTEGER primary key AUTOINCREMENT,
                    gender TEXT not null UNIQUE);''')
        print("Table professions was created")
        connection.commit()
        cursor.close()

# done
def add_new_gender(new_gender: str = None):
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        if new_gender:
            cursor.execute(f"""INSERT OR IGNORE INTO genders (gender) VALUES (?);""", (new_gender, ))
            print("Data into table genders was added")
        else:
            print(f'you have entered no parameters')
        connection.commit()
        cursor.close()

# done
def create_table_people():
    with sq.connect(name_of_db) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS people(
                    id INTEGER primary key AUTOINCREMENT,
                    name TEXT not null,
                    surname TEXT not null,
                    gender INTEGER REFERENCES genders (id) ON DELETE CASCADE ON UPDATE SET NULL,
                    salary INTEGER,
                    position INTEGER REFERENCES professions (id) ON UPDATE CASCADE ON UPDATE SET NULL ON DELETE SET NULL, 
                    email TEXT,
                    age INTEGER not null
                    );''')
        print("Table professions was created")
        connection.commit()
        cursor.close()

# done
def records_generator_people(number_of_records: int = 20):
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')

        for i in range(number_of_records):
            name = choice(NAMES_SET)
            surname = choice(SURNAMES_SET)
            gender = choice([choice(list(cursor.execute('SELECT id FROM genders')))[0], None])
            salary = choice([randint(10_000, 100_000), None])
            position = choice([choice(list(cursor.execute('SELECT id FROM professions')))[0], None])
            email = choice([str(f'{name[0]}.{surname}@ukr.net'), None])
            age = randint(*AGE_INTERVAL)

            cursor.execute(f"""INSERT INTO people  (name, surname, gender, salary, position, email, age) 
                                        VALUES ('{name}', '{surname}', ?, ?, ?, ?, {age});""",
                                                    (gender, salary, position, email))
        print(f"Data into table people was added ({number_of_records} rows were added)")
        connection.commit()
        cursor.close()


def add_new_person(name: str, surname: str, gender: (int, None), salary: (int, None), position: (int, None), email: (str, None), age: int):
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')

        name = name
        surname = surname
        gender = gender
        salary = salary
        position = position
        email = email
        age = age

        try:
            cursor.execute(f"""INSERT INTO people  (name, surname, gender, salary, position, email, age) 
                                        VALUES ('{name}', '{surname}', ?, ?, ?, ?, {age});""",
                                                    (gender, salary, position, email))
            print(f"You have added a new person {name} {surname}")
        except connection.IntegrityError:
            if gender:
                genders_primary_key = list(x[0] for x in list(map(list, cursor.execute('SELECT id FROM genders'))))
                if gender not in genders_primary_key:
                    print(f"We cannot add the record about {name} {surname} because you have entered the wrong gender key")

            if position:
                professions_primary_key = list(x[0] for x in list(map(list, cursor.execute('SELECT id FROM professions'))))
                if position not in professions_primary_key:
                    print(f"We cannot add the record about {name} {surname} because you have entered the wrong position key")

        connection.commit()
        cursor.close()


def amend_gender_by_surname(surname: str, new_gender: int):
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')

        try:
            cursor.execute(f"""
                        UPDATE people 
                        SET gender = '{new_gender}'
                        WHERE surname = '{surname}';""")
            print(f"You have successfully amended the gender of the person {surname}")
        except connection.IntegrityError:
            if new_gender:
                genders_primary_key = list(x[0] for x in list(map(list, cursor.execute('SELECT id FROM genders'))))
                if new_gender not in genders_primary_key:
                    print(f"We cannot amend the record about {surname} because you have entered the wrong gender key")
        connection.commit()
        cursor.close()


def choose_people_by_gender(gender: int):
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')
        data = tuple(cursor.execute(f"""
                    SELECT name, surname
                    FROM people  
                    WHERE gender = {gender};"""))

        if data:
            print("*"*100)

            for row in data:
                print(data.index(row)+1, *row)

            print(f'Data for people with gender key {gender}')
            print("*"*100)
        else:
            print("No data with your parameters")
        print("Function choose_people_by_gender was done")


def delete_records_from_table(table: str, identifier: int):
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')
        try:
            cursor.execute(f"""
                        DELETE
                        FROM {table}
                        WHERE id = {identifier};""")

            connection.commit()
            cursor.close()
            print(f"You have deleted from the table {table} one row")
        except sq.OperationalError:
            print("No data with your parameters")

        print("Delete record function was done")


def select_all_with_gender_and_profession_with_filter_salary_more_than(salary: int = 10_000):
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')
        data = list(cursor.execute(f"""
                    SELECT people.name, people.surname, people.salary, genders.gender, professions.profession 
                    FROM ((people
                    INNER JOIN genders ON people.gender = genders.id)
                    INNER JOIN professions ON people.position = professions.id)
                    WHERE people.salary > {salary};"""))
        
        if data:
            print("*"*100)
            print(f'There are next data than sasisfied your statements:')
            
            for _ in data:
                print(data.index(_) + 1, *_)

            print("*"*100)
        else:
            print('No data to print')
        connection.commit()
        cursor.close()


def select_all_with_gender_profession_not_required_with_filter_salary_more_than(salary: int = 10_000):
    with sq.connect(name_of_db) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')
        data = list(cursor.execute(f"""
                    SELECT people.name, people.surname, people.salary, genders.gender, professions.profession 
                    FROM ((people
                    INNER JOIN genders ON people.gender = genders.id)
                    LEFT JOIN professions ON people.position = professions.id)
                    WHERE people.salary > {salary};"""))
        
        if data:
            print("*"*100)
            print(f'There are next data than sasisfied your statements:')
            
            for _ in data:
                print(data.index(_) + 1, *_)
                
            print("*"*100)
        else:
            print('No data to print')
        connection.commit()
        cursor.close()


if __name__ == "__main__":
    print("This is work module for main running file advance sqlite3 homework")
