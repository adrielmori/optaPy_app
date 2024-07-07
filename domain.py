from datetime import date
from typing import List, Dict
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
from utils.utils import *
 

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
    def __init__(
        self,
        id: int,
        name: str,
        entry_date_core: date = date(9999, 1, 1),
        entry_date_inf: date = date(9999, 1, 1),
        nucleo: Nucleo = None,
    ):
        self.id = id
        self.name = name
        self.entry_date_core = entry_date_core
        self.entry_date_inf = entry_date_inf
        self.nucleo = nucleo

    @planning_id
    def get_id(self):
        return self.id

    def get_nucleo(self):
        return self.nucleo

    def get_entry_date_core(self):
        return self.entry_date_core

    def get_entry_date_inf(self):
        return self.entry_date_inf

    def __str__(self):
        return (
            f"Teacher(id={self.id}, "
            f"name={self.name}, "
            f"nucleo={self.nucleo}, "
            f"entry_date_core={self.entry_date_core}, "
            f"entry_date_inf={self.entry_date_inf})"
        )


@problem_fact
class Subject:
    def __init__(
        self,
        id: int,
        name: str,
        interested_teacher_ids=None,
        historical_teacher_ids=None,
        nucleo: Nucleo = None,
    ):
        self.id = id
        self.name = name
        self.interested_teacher_ids = (
            interested_teacher_ids if interested_teacher_ids is not None else []
        )
        self.historical_teacher_ids = (
            historical_teacher_ids if historical_teacher_ids is not None else []
        )
        self.nucleo = nucleo

    @planning_id
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_nucleo(self):
        return self.nucleo

    def get_interested_teacher_ids(self):
        return self.interested_teacher_ids

    def get_historical_teacher_ids(self):
        return self.historical_teacher_ids

    def add_interested_teacher(self, teacher):
        if teacher.id not in self.interested_teacher_ids:
            self.interested_teacher_ids.append(teacher.id)

    def is_teacher_interested(self, teacher):
        return teacher.id in self.interested_teacher_ids

    def add_historical_teacher_id(self, teacher):
        self.historical_teacher_ids.append(teacher.id)

    def __str__(self):
        return (
            f"Subject(id={self.id}, name={self.name}, "
            f"interested_teacher_ids={self.interested_teacher_ids}, "
            f"historical_teacher_ids={self.historical_teacher_ids}, "
            f"nucleo={self.nucleo})"
        )



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
    def __init__(
        self, lesson_list, teacher_list, subject_list, nucleo_list, score=None
    ):
        self.lesson_list = lesson_list
        self.subject_list = subject_list
        self.teacher_list = teacher_list
        self.nucleo_list = nucleo_list
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


def generate_domain_instances(json_disciplinas,  json_teacher, json_lessons, json_interest, year: int):
    nucleo_list = load_nucleo(json_disciplinas)
    subject_list = load_subject(json_disciplinas, nucleo_list)
    teacher_list = load_teachers(json_teacher, nucleo_list)
    lesson_list = load_lesson_list(json_lessons, subject_list, teacher_list)
    
    lesson_list.extend(load_lesson_interest_list(json_interest, lesson_list, subject_list, teacher_list, year))

    return lesson_list, teacher_list, subject_list, nucleo_list

def generate_problem(json: Dict):

    lesson_list, teacher_list, subject_list, nucleo_list = generate_domain_instances(
            json["disciplinas"], 
            json["docente"], 
            json["historico"],
            json["interessesDoDocente"],
            year=2024
        )

    return TimeTable(lesson_list, teacher_list, subject_list, nucleo_list)
