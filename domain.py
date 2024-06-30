from datetime import date
from typing import List
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


@problem_fact
class Teacher:
    def __init__(
        self,
        id: int,
        name: str,
        entry_date_core: date = None,
        entry_date_inf: date = None,
    ):
        self.id = id
        self.name = name
        self.entry_date_core = entry_date_core
        self.entry_date_inf = entry_date_inf

    @planning_id
    def get_id(self):
        return self.id

    def get_entry_date_core(self):
        return self.entry_date_core

    def get_entry_date_inf(self):
        return self.entry_date_inf

    def __str__(self):
        return (
            f"Teacher(id={self.id}, name={self.name}, "
            f"entry_date_core={self.entry_date_core}, "
            f"entry_date_inf={self.entry_date_inf})"
        )


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
    def __init__(
        self,
        id: int,
        year: int,
        subject: Subject,
        teacher: Teacher = None,
        teacher_list: List[Teacher] = None,
    ):
        self.id = id
        self.year = year
        self.subject = subject
        self.teacher = teacher
        self.teacher_list = teacher_list

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


def create_date(year: int, month: int) -> date:
    return date(year, month, 1)


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
        Teacher(
            1,
            "Plínio de Sá Leitão Júnior",
            create_date(2022, 12),
            create_date(2000, 10),
        ),
        Teacher(
            2, "Reinaldo de Souza Júnior", create_date(2021, 8), create_date(1987, 12)
        ),
        Teacher(
            3, "Fábio Nogueira de Lucena", create_date(2024, 1), create_date(1991, 12)
        ),
        Teacher(4, "Taciana Novo Kudo", create_date(2016, 3), create_date(1990, 2)),
        Teacher(5, "Renata Dutra Braga", create_date(2002, 8), create_date(1978, 12)),
        Teacher(
            6,
            "Ana Claudia Bastos Loureiro Monção",
            create_date(2011, 4),
            create_date(1994, 12),
        ),
        Teacher(
            7,
            "Sofia Larissa da Costa Paiva",
            create_date(2023, 8),
            create_date(1996, 12),
        ),
        Teacher(
            8, "Leonardo Andrade Ribeiro", create_date(2017, 8), create_date(1998, 12)
        ),
        Teacher(
            9, "Jacson Rodrigues Barbosa", create_date(2021, 2), create_date(1993, 2)
        ),
        Teacher(10, "Renato Bulcão", create_date(2021, 3), create_date(1993, 4)),
        Teacher(
            11, "Eliomar Araújo de Lima", create_date(2021, 5), create_date(1999, 12)
        ),
        Teacher(12, "Evellin Cardoso", create_date(2016, 8), create_date(1991, 7)),
        Teacher(
            13, "William Divino Ferreira", create_date(2017, 12), create_date(1987, 9)
        ),
        Teacher(
            14, "Rubens de Castro Pereira", create_date(2018, 8), create_date(2003, 2)
        ),
        Teacher(
            15,
            "Edison Andrade Martins Morais",
            create_date(2021, 1),
            create_date(1993, 1),
        ),
        Teacher(
            16,
            "Adailton Ferreira de Araújo",
            create_date(2023, 12),
            create_date(1993, 9),
        ),
        Teacher(17, "Hugo Nascimento", create_date(2022, 12), create_date(1993, 12)),
        Teacher(
            18, "Leonardo Antonio Alves", create_date(2023, 11), create_date(1993, 12)
        ),
        Teacher(
            19,
            "Juliano Lopes de Oliveira",
            create_date(2022, 12),
            create_date(1990, 1),
        ),
        Teacher(
            20,
            "Alessandro Cruvinel Machado de Araújo",
            create_date(2022, 12),
            create_date(2000, 12),
        ),
    ]
    lesson_list = [
        Lesson(1, 2020, subject_list[2], teacher_list[7], teacher_list),
        Lesson(2, 2020, subject_list[3], teacher_list[6], teacher_list),
        Lesson(3, 2020, subject_list[4], teacher_list[5], teacher_list),
        Lesson(4, 2020, subject_list[0], teacher_list[2], teacher_list),
        Lesson(5, 2020, subject_list[5], teacher_list[1], teacher_list),
        Lesson(6, 2020, subject_list[6], teacher_list[2], teacher_list),
        Lesson(7, 2020, subject_list[7], teacher_list[6], teacher_list),
        Lesson(8, 2020, subject_list[8], teacher_list[12], teacher_list),
        Lesson(9, 2020, subject_list[10], teacher_list[2], teacher_list),
        Lesson(10, 2020, subject_list[11], teacher_list[12], teacher_list),
        Lesson(11, 2020, subject_list[12], teacher_list[15], teacher_list),
        Lesson(12, 2020, subject_list[1], teacher_list[17], teacher_list),
        Lesson(13, 2020, subject_list[9], teacher_list[14], teacher_list),
        Lesson(14, 2021, subject_list[2], teacher_list[6], teacher_list),
        Lesson(15, 2021, subject_list[3], teacher_list[6], teacher_list),
        Lesson(16, 2021, subject_list[4], teacher_list[5], teacher_list),
        Lesson(17, 2021, subject_list[0], teacher_list[10], teacher_list),
        Lesson(18, 2021, subject_list[5], teacher_list[10], teacher_list),
        Lesson(19, 2021, subject_list[6], teacher_list[0], teacher_list),
        Lesson(20, 2021, subject_list[7], teacher_list[9], teacher_list),
        Lesson(21, 2021, subject_list[8], teacher_list[13], teacher_list),
        Lesson(22, 2021, subject_list[10], teacher_list[13], teacher_list),
        Lesson(23, 2021, subject_list[11], teacher_list[15], teacher_list),
        Lesson(24, 2021, subject_list[12], teacher_list[17], teacher_list),
        Lesson(25, 2021, subject_list[1], teacher_list[17], teacher_list),
        Lesson(26, 2021, subject_list[9], teacher_list[3], teacher_list),
        Lesson(27, 2022, subject_list[2], teacher_list[5], teacher_list),
        Lesson(28, 2022, subject_list[3], teacher_list[8], teacher_list),
        Lesson(29, 2022, subject_list[4], teacher_list[9], teacher_list),
        Lesson(30, 2022, subject_list[0], teacher_list[10], teacher_list),
        Lesson(31, 2022, subject_list[5], teacher_list[10], teacher_list),
        Lesson(32, 2022, subject_list[6], teacher_list[0], teacher_list),
        Lesson(33, 2022, subject_list[7], teacher_list[9], teacher_list),
        Lesson(34, 2022, subject_list[8], teacher_list[13], teacher_list),
        Lesson(35, 2022, subject_list[10], teacher_list[13], teacher_list),
        Lesson(36, 2022, subject_list[11], teacher_list[15], teacher_list),
        Lesson(37, 2022, subject_list[12], teacher_list[17], teacher_list),
        Lesson(38, 2022, subject_list[1], teacher_list[17], teacher_list),
        Lesson(39, 2022, subject_list[9], teacher_list[3], teacher_list),
        Lesson(40, 2023, subject_list[2], teacher_list[5], teacher_list),
        Lesson(41, 2023, subject_list[3], teacher_list[6], teacher_list),
        Lesson(42, 2023, subject_list[4], teacher_list[9], teacher_list),
        Lesson(43, 2023, subject_list[0], teacher_list[2], teacher_list),
        Lesson(44, 2023, subject_list[5], teacher_list[10], teacher_list),
        Lesson(45, 2023, subject_list[6], teacher_list[0], teacher_list),
        Lesson(46, 2023, subject_list[7], teacher_list[9], teacher_list),
        Lesson(47, 2023, subject_list[8], teacher_list[13], teacher_list),
        Lesson(48, 2023, subject_list[10], teacher_list[13], teacher_list),
        Lesson(49, 2023, subject_list[11], teacher_list[15], teacher_list),
        Lesson(50, 2023, subject_list[12], teacher_list[17], teacher_list),
        Lesson(51, 2023, subject_list[1], teacher_list[3], teacher_list),
        Lesson(52, 2023, subject_list[9], teacher_list[3], teacher_list),
        Lesson(
            53,
            2024,
            Subject(1, "INF0291", [1, 2, 3], [3, 11, 11, 3]),
            teacher_list=teacher_list,
        ),
        Lesson(
            54,
            2024,
            Subject(2, "INF0292", [4, 5], [18, 18, 18, 4]),
            teacher_list=teacher_list,
        ),
        Lesson(
            55,
            2024,
            Subject(3, "INF0287", [6, 7, 8], [8, 7, 6, 6]),
            teacher_list=teacher_list,
        ),
        Lesson(
            56,
            2024,
            Subject(4, "INF0018", [9, 7], [7, 7, 9, 9]),
            teacher_list=teacher_list,
        ),
        Lesson(
            57,
            2024,
            Subject(5, "INF0283", [7, 6, 10], [6, 6, 10, 10]),
            teacher_list=teacher_list,
        ),
        Lesson(
            58,
            2024,
            Subject(6, "INF0294", [11, 12], [2, 11, 11, 11]),
            teacher_list=teacher_list,
        ),
        Lesson(
            59,
            2024,
            Subject(7, "INF0056", [2, 1], [3, 1, 1, 1]),
            teacher_list=teacher_list,
        ),
        Lesson(
            60,
            2024,
            Subject(8, "INF0299", [10, 6, 7], [7, 10, 10, 10]),
            teacher_list=teacher_list,
        ),
        Lesson(
            61,
            2024,
            Subject(9, "INF0285", [13, 14], [13, 14, 14, 14]),
            teacher_list=teacher_list,
        ),
        Lesson(
            62,
            2024,
            Subject(10, "INF0293", [15, 4], [15, 4, 4, 4]),
            teacher_list=teacher_list,
        ),
        Lesson(
            63,
            2024,
            Subject(11, "INF0300", [16, 13], [3, 14, 14, 14]),
            teacher_list=teacher_list,
        ),
        Lesson(
            64,
            2024,
            Subject(12, "INF0284", [17, 18], [13, 16, 16, 16]),
            teacher_list=teacher_list,
        ),
        Lesson(
            65,
            2024,
            Subject(13, "INF0288", [19, 20], [16, 18, 18, 18]),
            teacher_list=teacher_list,
        ),
    ]

    return TimeTable(lesson_list, teacher_list, subject_list)
