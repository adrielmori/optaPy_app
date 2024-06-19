import datetime

import optapy
from optapy import problem_fact, planning_id, planning_entity, planning_variable, \
    planning_solution, planning_entity_collection_property, \
    problem_fact_collection_property, \
    value_range_provider, planning_score
from optapy.types import HardSoftScore
from datetime import time

@problem_fact
class Nucleo:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"Nucleo(id={self.id}, name={self.name})"

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
class Subjective:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"Subjective(id={self.id}, name={self.name})"

@planning_entity
class Lesson:
    def __init__(self, id: int, year: int, subject: Subjective, teacher: Teacher = None):
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
    return ',\n'.join(map(str, a_list))


@planning_solution
class TimeTable:
    teacher_list: list[Teacher]
    lesson_list: list[Lesson]
    score: HardSoftScore

    def __init__(self, teacher_list: list[Teacher], lesson_list: list[Lesson], score: HardSoftScore = None):
        self.teacher_list = teacher_list
        self.lesson_list = lesson_list
        self.score = score

    @problem_fact_collection_property(Teacher)
    @value_range_provider("teacherRange")
    def get_teacher_list(self):
        return self.teacher_list
    
    @planning_entity_collection_property(Lesson)
    def get_lesson_list(self):
        return self.lesson_list


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
    subjective_list = [
        Subjective(1, "INF0291"),
        Subjective(2, "INF0292"),
        Subjective(3, "INF0287"),
        Subjective(4, "INF0018"),
        Subjective(5, "INF0283"),
        Subjective(6, "INF0294"),
        Subjective(7, "INF0056"),
        Subjective(8, "INF0299"),
        Subjective(9, "INF0285"),
        Subjective(10, "INF0293"),
        Subjective(11, "INF0300"),
        Subjective(12, "INF0284"),
        Subjective(13, "INF0288"),
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
        Lesson(1, 2020, Subjective(3, "INF0287"), Teacher(8, "Leonardo Andrade Ribeiro")),
        Lesson(2, 2020, Subjective(4, "INF0018"), Teacher(7, "Sofia Larissa da Costa Paiva")),
        Lesson(3, 2020, Subjective(5, "INF0283"), Teacher(6, "Ana Claudia Bastos Loureiro Monção")),
        Lesson(4, 2020, Subjective(1, "INF0291"), Teacher(3, "Fábio Nogueira de Lucena")),
        Lesson(5, 2020, Subjective(6, "INF0294"), Teacher(2, "Reinaldo de Souza Júnior")),
        Lesson(6, 2020, Subjective(7, "INF0056"), Teacher(3, "Fábio Nogueira de Lucena")),
        Lesson(7, 2020, Subjective(8, "INF0299"), Teacher(7, "Sofia Larissa da Costa Paiva")),
        Lesson(8, 2020, Subjective(9, "INF0285"), Teacher(13, "William Divino Ferreira")),
        Lesson(9, 2020, Subjective(11, "INF0300"), Teacher(3, "Fábio Nogueira de Lucena")),
        Lesson(10, 2020, Subjective(12, "INF0284"), Teacher(13, "William Divino Ferreira")),
        Lesson(11, 2020, Subjective(13, "INF0288"), Teacher(16, "Adailton Ferreira de Araújo")),
        Lesson(12, 2020, Subjective(2, "INF0292"), Teacher(18, "Leonardo Antonio Alves")),
        Lesson(13, 2020, Subjective(10, "INF0293"), Teacher(15, "Edison Andrade Martins Morais")),
        Lesson(14, 2021, Subjective(3, "INF0287"), Teacher(7, "Sofia Larissa da Costa Paiva")),
        Lesson(15, 2021, Subjective(4, "INF0018"), Teacher(7, "Sofia Larissa da Costa Paiva")),
        Lesson(16, 2021, Subjective(5, "INF0283"), Teacher(6, "Ana Claudia Bastos Loureiro Monção")),
        Lesson(17, 2021, Subjective(1, "INF0291"), Teacher(11, "Eliomar Araújo de Lima")),
        Lesson(18, 2021, Subjective(6, "INF0294"), Teacher(11, "Eliomar Araújo de Lima")),
        Lesson(19, 2021, Subjective(7, "INF0056"), Teacher(1, "Plínio de Sá Leitão Júnior")),
        Lesson(20, 2021, Subjective(8, "INF0299"), Teacher(10, "Renato Bulcão")),
        Lesson(21, 2021, Subjective(9, "INF0285"), Teacher(14, "Rubens de Castro Pereira")),
        Lesson(22, 2021, Subjective(11, "INF0300"), Teacher(14, "Rubens de Castro Pereira")),
        Lesson(23, 2021, Subjective(12, "INF0284"), Teacher(16, "Adailton Ferreira de Araújo")),
        Lesson(24, 2021, Subjective(13, "INF0288"), Teacher(18, "Leonardo Antonio Alves")),
        Lesson(25, 2021, Subjective(2, "INF0292"), Teacher(18, "Leonardo Antonio Alves")),
        Lesson(26, 2021, Subjective(10, "INF0293"), Teacher(4, "Taciana Novo Kudo")),
        Lesson(27, 2022, Subjective(3, "INF0287"), Teacher(6, "Ana Claudia Bastos Loureiro Monção")),
        Lesson(28, 2022, Subjective(4, "INF0018"), Teacher(9, "Jacson Rodrigues Barbosa")),
        Lesson(29, 2022, Subjective(5, "INF0283"), Teacher(10, "Renato Bulcão")),
        Lesson(30, 2022, Subjective(1, "INF0291"), Teacher(11, "Eliomar Araújo de Lima")),
        Lesson(31, 2022, Subjective(6, "INF0294"), Teacher(11, "Eliomar Araújo de Lima")),
        Lesson(32, 2022, Subjective(7, "INF0056"), Teacher(1, "Plínio de Sá Leitão Júnior")),
        Lesson(33, 2022, Subjective(8, "INF0299"), Teacher(10, "Renato Bulcão")),
        Lesson(34, 2022, Subjective(9, "INF0285"), Teacher(14, "Rubens de Castro Pereira")),
        Lesson(35, 2022, Subjective(11, "INF0300"), Teacher(14, "Rubens de Castro Pereira")),
        Lesson(36, 2022, Subjective(12, "INF0284"), Teacher(16, "Adailton Ferreira de Araújo")),
        Lesson(37, 2022, Subjective(13, "INF0288"), Teacher(18, "Leonardo Antonio Alves")),
        Lesson(38, 2022, Subjective(2, "INF0292"), Teacher(18, "Leonardo Antonio Alves")),
        Lesson(39, 2022, Subjective(10, "INF0293"), Teacher(4, "Taciana Novo Kudo")),
        Lesson(40, 2023, Subjective(3, "INF0287"), Teacher(6, "Ana Claudia Bastos Loureiro Monção")),
        Lesson(41, 2023, Subjective(4, "INF0018"), Teacher(9, "Jacson Rodrigues Barbosa")),
        Lesson(42, 2023, Subjective(5, "INF0283"), Teacher(10, "Renato Bulcão")),
        Lesson(43, 2023, Subjective(1, "INF0291"), Teacher(3, "Fábio Nogueira de Lucena")),
        Lesson(44, 2023, Subjective(6, "INF0294"), Teacher(11, "Eliomar Araújo de Lima")),
        Lesson(45, 2023, Subjective(7, "INF0056"), Teacher(1, "Plínio de Sá Leitão Júnior")),
        Lesson(46, 2023, Subjective(8, "INF0299"), Teacher(10, "Renato Bulcão")),
        Lesson(47, 2023, Subjective(9, "INF0285"), Teacher(14, "Rubens de Castro Pereira")),
        Lesson(48, 2023, Subjective(11, "INF0300"), Teacher(14, "Rubens de Castro Pereira")),
        Lesson(49, 2023, Subjective(12, "INF0284"), Teacher(16, "Adailton Ferreira de Araújo")),
        Lesson(50, 2023, Subjective(13, "INF0288"), Teacher(18, "Leonardo Antonio Alves")),
        Lesson(51, 2023, Subjective(2, "INF0292"), Teacher(4, "Taciana Novo Kudo")),
        Lesson(52, 2023, Subjective(10, "INF0293"), Teacher(4, "Taciana Novo Kudo")),
        Lesson(53, 2024, Subjective(3, "INF0287")),
        Lesson(54, 2024, Subjective(4, "INF0018")),
        Lesson(55, 2024, Subjective(5, "INF0283")),
        Lesson(56, 2024, Subjective(1, "INF0291")),
        Lesson(57, 2024, Subjective(6, "INF0294")),
        Lesson(58, 2024, Subjective(7, "INF0056")),
        Lesson(59, 2024, Subjective(8, "INF0299")),
        Lesson(60, 2024, Subjective(9, "INF0285")),
        Lesson(61, 2024, Subjective(11, "INF0300")),
        Lesson(62, 2024, Subjective(12, "INF0284")),
        Lesson(63, 2024, Subjective(13, "INF0288")),
        Lesson(64, 2024, Subjective(2, "INF0292")),
        Lesson(65, 2024, Subjective(10, "INF0293")),
    ]

    # interest_lesson_list = [
    #     Interest(Subjective(1, "INF0291"), Teacher(1, "Plínio de Sá Leitão Júnior")),
    #     Interest(Subjective(1, "INF0291"), Teacher(2, "Reinaldo de Souza Júnior")),
    #     Interest(Subjective(1, "INF0291"), Teacher(3, "Fábio Nogueira de Lucena")),
    #     Interest(Subjective(2, "INF0292"), Teacher(4, "Taciana Novo Kudo")),
    #     Interest(Subjective(2, "INF0292"), Teacher(5, "Renata Dutra Braga")),
    #     Interest(Subjective(3, "INF0287"), Teacher(6, "Ana Claudia Bastos Loureiro Monção")),
    #     Interest(Subjective(3, "INF0287"), Teacher(7, "Sofia Larissa da Costa Paiva")),
    #     Interest(Subjective(3, "INF0287"), Teacher(8, "Leonardo Andrade Ribeiro")),
    #     Interest(Subjective(4, "INF0018"), Teacher(9, "Jacson Rodrigues Barbosa")),
    #     Interest(Subjective(4, "INF0018"), Teacher(7, "Sofia Larissa da Costa Paiva")),
    #     Interest(Subjective(5, "INF0283"), Teacher(7, "Sofia Larissa da Costa Paiva")),
    #     Interest(Subjective(5, "INF0283"), Teacher(6, "Ana Claudia Bastos Loureiro Monção")),
    #     Interest(Subjective(5, "INF0283"), Teacher(10, "Renato Bulcão")),
    #     Interest(Subjective(6, "INF0294"), Teacher(11, "Eliomar Araújo de Lima")),
    #     Interest(Subjective(6, "INF0294"), Teacher(12, "Evellin Cardoso")),
    #     Interest(Subjective(7, "INF0056"), Teacher(2, "Reinaldo de Souza Júnior")),
    #     Interest(Subjective(7, "INF0056"), Teacher(1, "Plínio de Sá Leitão Júnior")),
    #     Interest(Subjective(8, "INF0299"), Teacher(10, "Renato Bulcão")),
    #     Interest(Subjective(8, "INF0299"), Teacher(6, "Ana Claudia Bastos Loureiro Monção")),
    #     Interest(Subjective(8, "INF0299"), Teacher(7, "Sofia Larissa da Costa Paiva")),
    #     Interest(Subjective(9, "INF0285"), Teacher(13, "William Divino Ferreira")),
    #     Interest(Subjective(9, "INF0285"), Teacher(14, "Rubens de Castro Pereira")),
    #     Interest(Subjective(10, "INF0293"), Teacher(15, "Edison Andrade Martins Morais")),
    #     Interest(Subjective(10, "INF0293"), Teacher(4, "Taciana Novo Kudo")),
    #     Interest(Subjective(11, "INF0300"), Teacher(16, "Adailton Ferreira de Araújo")),
    #     Interest(Subjective(11, "INF0300"), Teacher(13, "William Divino Ferreira")),
    #     Interest(Subjective(12, "INF0284"), Teacher(17, "Hugo Nascimento")),
    #     Interest(Subjective(12, "INF0284"), Teacher(18, "Leonardo Antonio Alves")),
    #     Interest(Subjective(13, "INF0288"), Teacher(19, "Juliano Lopes de Oliveira")),
    #     Interest(Subjective(13, "INF0288"), Teacher(20, "Alessandro Cruvinel Machado de Araújo")),
    # ]


    return TimeTable(teacher_list, lesson_list)