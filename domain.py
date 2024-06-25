from optapy import (
    planning_solution,
    planning_entity_collection_property,
    planning_score,
    problem_fact,
    planning_id,
    planning_entity,
    planning_variable,
    problem_fact_collection_property,
    value_range_provider,
)
from optapy.score import HardSoftScore
from datetime import time


@problem_fact
class Teacher:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"Teacher(id={self.id}, name={self.name})"


@problem_fact
class Subject:
    def __init__(
        self, id, name, interested_teacher_ids=None, historical_teacher_ids=None
    ):
        self.id = id
        self.name = name
        self.interested_teacher_ids = (
            interested_teacher_ids if interested_teacher_ids is not None else []
        )
        self.historical_teacher_ids = (
            historical_teacher_ids if historical_teacher_ids is not None else []
        )

    @planning_id
    def get_id(self):
        return self.id

    def add_interested_teacher(self, teacher):
        if teacher.id not in self.interested_teacher_ids:
            self.interested_teacher_ids.append(teacher.id)

    def is_teacher_interested(self, teacher):
        return teacher.id in self.interested_teacher_ids

    def add_historical_teacher_id(self, teacher):
        if teacher.id not in self.historical_teacher_ids:
            self.historical_teacher_ids.append(teacher.id)

    def __str__(self):
        return f"Subject(id={self.id}, name={self.name}, interested_teacher_ids={self.interested_teacher_ids}, historical_teacher_ids={self.historical_teacher_ids})"


@planning_entity
class Lesson:
    def __init__(self, id: int, year: int, subject: Subject, teacher: Teacher = None):
        self.id = id
        self.year = year
        self.subject = subject
        self.teacher = teacher

    @planning_id
    def get_id(self):
        return self.id

    @planning_variable(Teacher, ["teacherRange"])
    def get_teacher(self):
        return self.teacher

    def set_teacher(self, new_teacher):
        self.teacher = new_teacher

    def __str__(self):
        return (
            f"Lesson("
            f"id={self.id}, "
            f"subject={self.subject}, "
            f"year={self.year}, "
            f"teacher={self.teacher}"
            f")"
        )


def format_list(a_list):
    return ",\n".join(map(str, a_list))


@planning_solution
class TimeTable:
    def __init__(self, lesson_list, teacher_list, subject_list, score=None):
        self.lesson_list = lesson_list
        self.subject_list = subject_list
        self.teacher_list = teacher_list
        self.score = score

    @planning_entity_collection_property(Lesson)
    def get_lesson_list(self):
        return self.lesson_list

    @problem_fact_collection_property(Teacher)
    @value_range_provider("teacherRange")
    def get_teacher_list(self):
        return self.teacher_list

    @planning_score(HardSoftScore)
    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def __str__(self):
        return (
            f"TimeTable("
            f"teacher_list={format_list(self.teacher_list)},\n"
            f"lesson_list={format_list(self.lesson_list)},\n"
            f"score={str(self.score.toString()) if self.score is not None else 'None'}"
            f")"
        )


def generate_problem():
    subject_list = [
        Subject(1, "INF0291"),
        Subject(2, "INF0292"),
        Subject(3, "INF0287"),
        Subject(4, "INF0018"),
        Subject(5, "INF0283"),
        Subject(6, "INF0294"),
        Subject(7, "INF0056"),
        Subject(8, "INF0299"),
        Subject(9, "INF0285"),
        Subject(10, "INF0293"),
        Subject(11, "INF0300"),
        Subject(12, "INF0284"),
        Subject(13, "INF0288"),
    ]
    teacher_list = [
        Teacher(1, "Plínio de Sá Leitão Júnior"),
        Teacher(2, "Reinaldo de Souza Júnior"),
        Teacher(3, "Fábio Nogueira de Lucena"),
        Teacher(4, "Taciana Novo Kudo"),
        Teacher(5, "Renata Dutra Braga"),
        Teacher(6, "Ana Claudia Bastos Loureiro Monção"),
        Teacher(7, "Sofia Larissa da Costa Paiva"),
        Teacher(8, "Leonardo Andrade Ribeiro"),
        Teacher(9, "Jacson Rodrigues Barbosa"),
        Teacher(10, "Renato Bulcão"),
        Teacher(11, "Eliomar Araújo de Lima"),
        Teacher(12, "Evellin Cardoso"),
        Teacher(13, "William Divino Ferreira"),
        Teacher(14, "Rubens de Castro Pereira"),
        Teacher(15, "Edison Andrade Martins Morais"),
        Teacher(16, "Adailton Ferreira de Araújo"),
        Teacher(17, "Hugo Nascimento"),
        Teacher(18, "Leonardo Antonio Alves"),
        Teacher(19, "Juliano Lopes de Oliveira"),
        Teacher(20, "Alessandro Cruvinel Machado de Araújo"),
    ]
    lesson_list = [
        Lesson(1, 2020, Subject(3, "INF0287"), teacher_list[7]),
        Lesson(2, 2020, Subject(4, "INF0018"), teacher_list[6]),
        Lesson(3, 2020, Subject(5, "INF0283"), teacher_list[5]),
        Lesson(4, 2020, Subject(1, "INF0291"), teacher_list[2]),
        Lesson(5, 2020, Subject(6, "INF0294"), teacher_list[1]),
        Lesson(6, 2020, Subject(7, "INF0056"), teacher_list[2]),
        Lesson(7, 2020, Subject(8, "INF0299"), teacher_list[6]),
        Lesson(8, 2020, Subject(9, "INF0285"), teacher_list[12]),
        Lesson(9, 2020, Subject(11, "INF0300"), teacher_list[2]),
        Lesson(10, 2020, Subject(12, "INF0284"), teacher_list[12]),
        Lesson(11, 2020, Subject(13, "INF0288"), teacher_list[15]),
        Lesson(12, 2020, Subject(2, "INF0292"), teacher_list[17]),
        Lesson(13, 2020, Subject(10, "INF0293"), teacher_list[14]),
        Lesson(14, 2021, Subject(3, "INF0287"), teacher_list[6]),
        Lesson(15, 2021, Subject(4, "INF0018"), teacher_list[6]),
        Lesson(16, 2021, Subject(5, "INF0283"), teacher_list[5]),
        Lesson(17, 2021, Subject(1, "INF0291"), teacher_list[10]),
        Lesson(18, 2021, Subject(6, "INF0294"), teacher_list[10]),
        Lesson(19, 2021, Subject(7, "INF0056"), teacher_list[0]),
        Lesson(20, 2021, Subject(8, "INF0299"), teacher_list[9]),
        Lesson(21, 2021, Subject(9, "INF0285"), teacher_list[13]),
        Lesson(22, 2021, Subject(11, "INF0300"), teacher_list[13]),
        Lesson(23, 2021, Subject(12, "INF0284"), teacher_list[15]),
        Lesson(24, 2021, Subject(13, "INF0288"), teacher_list[17]),
        Lesson(25, 2021, Subject(2, "INF0292"), teacher_list[17]),
        Lesson(26, 2021, Subject(10, "INF0293"), teacher_list[3]),
        Lesson(27, 2022, Subject(3, "INF0287"), teacher_list[5]),
        Lesson(28, 2022, Subject(4, "INF0018"), teacher_list[8]),
        Lesson(29, 2022, Subject(5, "INF0283"), teacher_list[9]),
        Lesson(30, 2022, Subject(1, "INF0291"), teacher_list[10]),
        Lesson(31, 2022, Subject(6, "INF0294"), teacher_list[10]),
        Lesson(32, 2022, Subject(7, "INF0056"), teacher_list[0]),
        Lesson(33, 2022, Subject(8, "INF0299"), teacher_list[9]),
        Lesson(34, 2022, Subject(9, "INF0285"), teacher_list[13]),
        Lesson(35, 2022, Subject(11, "INF0300"), teacher_list[13]),
        Lesson(36, 2022, Subject(12, "INF0284"), teacher_list[15]),
        Lesson(37, 2022, Subject(13, "INF0288"), teacher_list[17]),
        Lesson(38, 2022, Subject(2, "INF0292"), teacher_list[17]),
        Lesson(39, 2022, Subject(10, "INF0293"), teacher_list[3]),
        Lesson(40, 2023, Subject(3, "INF0287"), teacher_list[5]),
        Lesson(41, 2023, Subject(4, "INF0018"), teacher_list[6]),
        Lesson(42, 2023, Subject(5, "INF0283"), teacher_list[9]),
        Lesson(43, 2023, Subject(1, "INF0291"), teacher_list[2]),
        Lesson(44, 2023, Subject(6, "INF0294"), teacher_list[10]),
        Lesson(45, 2023, Subject(7, "INF0056"), teacher_list[0]),
        Lesson(46, 2023, Subject(8, "INF0299"), teacher_list[9]),
        Lesson(47, 2023, Subject(9, "INF0285"), teacher_list[13]),
        Lesson(48, 2023, Subject(11, "INF0300"), teacher_list[13]),
        Lesson(49, 2023, Subject(12, "INF0284"), teacher_list[15]),
        Lesson(50, 2023, Subject(13, "INF0288"), teacher_list[17]),
        Lesson(51, 2023, Subject(2, "INF0292"), teacher_list[3]),
        Lesson(52, 2023, Subject(10, "INF0293"), teacher_list[3]),
        Lesson(53, 2024, Subject(3, "INF0287", [6, 7, 8], [8, 7, 6, 6])),
        Lesson(54, 2024, Subject(4, "INF0018", [9, 7], [7, 7, 9, 9])),
        Lesson(55, 2024, Subject(5, "INF0283", [7, 6, 10], [6, 6, 10, 10])),
        Lesson(56, 2024, Subject(1, "INF0291", [1, 2, 3], [3, 11, 11, 3])),
        Lesson(57, 2024, Subject(6, "INF0294", [11, 12], [2, 11, 11, 11])),
        Lesson(58, 2024, Subject(7, "INF0056", [2, 1], [3, 1, 1, 1])),
        Lesson(59, 2024, Subject(8, "INF0299", [10, 6, 7], [7, 10, 10, 10])),
        Lesson(60, 2024, Subject(9, "INF0285", [13, 14], [13, 14, 14, 14])),
        Lesson(61, 2024, Subject(11, "INF0300", [16, 13], [3, 14, 14, 14])),
        Lesson(62, 2024, Subject(12, "INF0284", [17, 18], [13, 16, 16, 16])),
        Lesson(63, 2024, Subject(13, "INF0288", [19, 20], [16, 18, 18, 18])),
        Lesson(64, 2024, Subject(2, "INF0292", [4, 5], [18, 18, 18, 4])),
        Lesson(65, 2024, Subject(10, "INF0293", [15, 4], [15, 4, 4, 4])),
    ]

    return TimeTable(lesson_list, teacher_list, subject_list)
