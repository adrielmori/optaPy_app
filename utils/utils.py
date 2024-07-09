from typing import List, Dict
from datetime import datetime

import domain

def create_date(year, month):
    #TODO: Retorna um objeto datetime a partir do ano e mês fornecidos.
    return datetime(year, month, 1)

def load_nucleo(data: Dict):
    #TODO: Cria uma lista de objetos Nucleo a partir dos dados fornecidos.
    from domain import Nucleo

    nucleo_list = []
    nucleo_ids = set()
    for item in data:
        if item['nucleoId'] not in nucleo_ids:
            nucleo = Nucleo(item['id'], item['nucleoId'])
            nucleo_list.append(nucleo)
            nucleo_ids.add(item['nucleoId'])
    return nucleo_list

def load_subject(data: Dict, nucleo_list: List):
    #TODO: Retorna um objeto datetime a partir do ano e mês fornecidos.
    from domain import Subject

    subject_list = []
    nucleo_dict = {nucleo.name: nucleo for nucleo in nucleo_list}
    for item in data:
        if item['nucleoId'] in nucleo_dict:
            subject = Subject(item['id'], item['codDisc'], nucleo=nucleo_dict[item['nucleoId']])
            subject_list.append(subject)
    return subject_list


def load_teachers(data: Dict, nucleo_list: List):
    #TODO: Cria uma lista de objetos Nucleo a partir dos dados fornecidos.
    from domain import Teacher
    teacher_list = []
    nucleo_dict = {nucleo.name: nucleo for nucleo in nucleo_list}
    for id, item in data.items():
        if item['nucleoId'] in nucleo_dict:
            dataNucleo = datetime.strptime(item['dataNucleo'], '%Y-%m-%d')
            dataInf = datetime.strptime(item['dataInf'], '%Y-%m-%d')
            teacher = Teacher(int(id), item['nome'], dataNucleo, dataInf,
                              nucleo=nucleo_dict[item['nucleoId']])
            teacher_list.append(teacher)
    return teacher_list


def load_lesson_list(data: Dict, subject_list: List, teacher_list: List):
    #TODO: Cria uma lista de objetos Lesson a partir dos dados, da lista de Subject e da lista de Teacher fornecidos.
    from domain import Lesson
    lesson_list_historic = []
    subject_dict = {subject.id: subject for subject in subject_list}
    teacher_dict = {teacher.id: teacher for teacher in teacher_list}
    for year, lessons in data.items():
        for lesson in lessons:
            if lesson['idDisc'] in subject_dict and lesson['idProfessor'] in teacher_dict:
                lesson_obj = Lesson(len(lesson_list_historic) + 1, int(year), subject_dict[lesson['idDisc']], teacher_dict[lesson['idProfessor']], teacher_list)
                lesson_list_historic.append(lesson_obj)
    return lesson_list_historic


def load_lesson_interest_list(data: Dict, lesson_list : List, subject_list: List, teacher_list: List, year: int):
    #TODO: Cria uma lista de objetos Lesson para um determinado ano a partir dos dados, da lista de Lesson, da lista de Subject e da lista de Teacher fornecidos.
    from domain import Lesson, Subject

    lesson_list_solver = []
    subject_dict = {subject.id: subject for subject in subject_list}
    teacher_dict = {teacher.id: teacher for teacher in teacher_list}
    id = lesson_list[-1].id + 1 if lesson_list else 1
    
    def get_interested_teachers(disc_id):
        #TODO: Retorna uma lista de IDs de professores interessados em uma determinada disciplina.
        return [item['idProfessor'] for item in data if disc_id in item['interresseDisciplina']]

    def get_historical_teachers(disc_id):
        #TODO: Retorna uma lista de IDs de professores que lecionaram uma determinada disciplina no passado.
        return [lesson.teacher.id for lesson in lesson_list if lesson.subject.id == disc_id]

    for disc in subject_dict.values():
        list_interets = get_interested_teachers(disc.id)
        list_teacher_historical = get_historical_teachers(disc.id)
        teacher = teacher_dict[list_interets[0]] if list_interets else None
        if teacher:
            cod = disc.name
            lesson = Lesson(id, year, Subject(disc.id, disc.name, list_interets, list_teacher_historical, disc.nucleo), 
                            teacher, teacher_list)
            lesson_list_solver.append(lesson)
            id += 1
    return lesson_list_solver

def print_timetable(lesson_list):
    lesson_list_2024 = list(
        filter(lambda the_lesson: the_lesson.year == 2024, lesson_list)
    )

    print("|-------------------|-------------------|")
    print("| Subject           | Teacher           |")
    print("|-------------------|-------------------|")
    for lesson in lesson_list_2024:
        out = "| " + "{:<15}".format(lesson.subject.name)[0:15] + " | "
        out += "{:<15}".format(lesson.teacher.name)[0:15] + " | "
        print(out)
    print("|-------------------|-------------------|")

    unassigned_lessons = list(
        filter(
            lambda unassigned_lesson: unassigned_lesson.year == 2024
            and unassigned_lesson.teacher is None,
            lesson_list,
        )
    )
    if len(unassigned_lessons) > 0:
        print()
        print("Unassigned lessons")
        for lesson in unassigned_lessons:
            print(" " + lesson.subject.name + " - No teacher assigned")


def timetable_to_json(lesson_list, timetabling_score):
    lesson_list_2024 = list(
        filter(lambda the_lesson: the_lesson.year == 2024, lesson_list)
    )

    timetable_json = {"lessons": [], "score": str(timetabling_score)}
    for lesson in lesson_list_2024:
        lesson_json = {
            "Subject": lesson.subject.name,
            "Teacher": lesson.teacher.name
        }
        timetable_json["lessons"].append(lesson_json)

    unassigned_lessons = list(
        filter(
            lambda unassigned_lesson: unassigned_lesson.year == 2024
            and unassigned_lesson.teacher is None,
            lesson_list,
        )
    )
    if len(unassigned_lessons) > 0:
        timetable_json["unassigned_lessons"] = []
        for lesson in unassigned_lessons:
            lesson_json = {
                "Subject": lesson.subject.name,
                "Teacher": "No teacher assigned"
            }
            timetable_json["unassigned_lessons"].append(lesson_json)

    return timetable_json
