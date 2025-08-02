import mysql.connector
import random
from faker import Faker


class StudentDataGenerator:
    def __init__(self, num_students=30):
        self.fake = Faker()
        self.num_students = num_students

    def generate_data(self):
        students = []
        programming = []
        soft_skills = []
        placement = []

        companies = ['Infosys', 'TCS', 'Wipro', 'Accenture', 'Google', 'Not Placed']

        for sid in range(4001, 4001 + self.num_students):
            gender = random.choice(['Male', 'Female'])
            name = self.fake.name_male() if gender == 'Male' else self.fake.name_female()
            email = self.fake.email()
            city = self.fake.city()
            enrollment_year = random.randint(2019, 2022)
            age = random.randint(18, 25)

            students.append((sid, name, age, gender, email, city, enrollment_year))

            programming.append((
                sid,
                random.randint(50, 100),
                random.randint(40, 100),
                random.randint(40, 100),
                random.randint(50, 100)
            ))

            soft_skills.append((
                sid,
                random.randint(60, 100),
                random.randint(60, 100),
                random.randint(50, 100)
            ))

            company = random.choice(companies)
            package = round(random.uniform(3, 20), 1) if company != 'Not Placed' else None
            placement_year = enrollment_year + 3

            placement.append((sid, company, package, placement_year))

        return students, programming, soft_skills, placement


class StudentDatabaseManager:
    def __init__(self, host='localhost', user='root', password='123456789', database='students_db'):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                student_id INT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                gender VARCHAR(10),
                email VARCHAR(100),
                city VARCHAR(100),
                enrollment_year INT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Programming (
                student_id INT PRIMARY KEY,
                python INT,
                java INT,
                cplusplus INT,
                web_dev INT,
                FOREIGN KEY (student_id) REFERENCES Students(student_id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS SoftSkills (
                student_id INT PRIMARY KEY,
                communication INT,
                teamwork INT,
                leadership INT,
                FOREIGN KEY (student_id) REFERENCES Students(student_id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Placement (
                student_id INT PRIMARY KEY,
                company VARCHAR(100),
                package FLOAT,
                placement_year INT,
                FOREIGN KEY (student_id) REFERENCES Students(student_id)
            )
        ''')
        self.conn.commit()

    def insert_data(self, students, programming, soft_skills, placement):
        self.cursor.executemany(
            "INSERT INTO Students (student_id, name, age, gender, email, city, enrollment_year) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            students
        )
        self.cursor.executemany(
            "INSERT INTO Programming (student_id, python, java, cplusplus, web_dev) VALUES (%s, %s, %s, %s, %s)",
            programming
        )
        self.cursor.executemany(
            "INSERT INTO SoftSkills (student_id, communication, teamwork, leadership) VALUES (%s, %s, %s, %s)",
            soft_skills
        )
        self.cursor.executemany(
            "INSERT INTO Placement (student_id, company, package, placement_year) VALUES (%s, %s, %s, %s)",
            placement
        )
        self.conn.commit()

    def delete_all_data(self):
        self.cursor.execute("DELETE FROM Placement")
        self.cursor.execute("DELETE FROM SoftSkills")
        self.cursor.execute("DELETE FROM Programming")
        self.cursor.execute("DELETE FROM Students")
        self.conn.commit()
        print("🗑️ All data deleted from all tables.")

    def close(self):
        self.cursor.close()
        self.conn.close()


# === Main Execution ===
if __name__ == "__main__":
    generator = StudentDataGenerator(num_students=30)
    students, programming, soft_skills, placement = generator.generate_data()

    db = StudentDatabaseManager()
    db.create_tables()
    db.delete_all_data()
    db.insert_data(students, programming, soft_skills, placement)
    db.close()

    print("✔️ Data inserted successfully into MySQL database 'students_db'")