import sqlite3
from faker import Faker
import random


class UniversityDB:
    def __init__(
        self,
        db_name="universita.db",
        num_students=1000,
        num_courses=10,
        num_iscrizioni=3000,
    ):
        self.db_name = db_name
        self.num_students = num_students
        self.num_courses = num_courses
        self.num_iscrizioni = num_iscrizioni
        self.fake = Faker()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.populate_tables()

    def create_tables(self):
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Students (
            StudentID INT PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            BirthDate DATE,
            IscrizioniDate DATE
        );
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Courses (
            CourseID INT PRIMARY KEY,
            CourseName VARCHAR(50),
            Credits INT
        );
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Iscrizioni (
            IscrizioniID INT PRIMARY KEY,
            StudentID INT,
            CourseID INT,
            Grade CHAR(1),
            FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
        );
        """
        )

    def populate_tables(self):
        students_data = [
            (
                i,
                self.fake.first_name(),
                self.fake.last_name(),
                self.fake.date_of_birth(minimum_age=18, maximum_age=30).isoformat(),
                self.fake.date_this_decade().isoformat(),
            )
            for i in range(1, self.num_students + 1)
        ]
        courses_data = [
            (i, self.fake.word().capitalize(), random.randint(1, 6))
            for i in range(1, self.num_courses + 1)
        ]
        grade_choices = ["A", "B", "C", "D", "F"]
        iscrizioni_data = [
            (
                i,
                random.randint(1, self.num_students),
                random.randint(1, self.num_courses),
                random.choice(grade_choices),
            )
            for i in range(1, self.num_iscrizioni + 1)
        ]

        self.cursor.executemany(
            "INSERT OR IGNORE INTO Students VALUES (?, ?, ?, ?, ?)", students_data
        )
        self.cursor.executemany(
            "INSERT OR IGNORE INTO Courses VALUES (?, ?, ?)", courses_data
        )
        self.cursor.executemany(
            "INSERT OR IGNORE INTO Iscrizioni VALUES (?, ?, ?, ?)", iscrizioni_data
        )

        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = UniversityDB()
    db.close()
