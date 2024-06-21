from datetime import datetime, date, timedelta
from optapy import constraint_provider, get_class
from optapy.constraint import ConstraintFactory, Joiners
from optapy.score import HardSoftScore
from domain import Lesson, Subjective, Teacher, Nucleo
from utils import *

# TODO: ID disciplina, Code disciplina, List(): Id Professores interessados
possibilite_lesson_list = [
    (1, "INF0291", [1, 2, 3]),
    (2, "INF0292", [4, 5]),
    (3, "INF0287", [6, 7, 8]),
    (4, "INF0018", [9, 7]),
    (5, "INF0283", [7, 6, 10]),
    (6, "INF0294", [11, 12]),
    (7, "INF0056", [2, 1]),
    (8, "INF0299", [10, 6, 7]),
    (9, "INF0285", [13, 14]),
    (10, "INF0293", [15, 4]),
    (11, "INF0300", [16, 13]),
    (12, "INF0284", [17, 18]),
    (13, "INF0288", [19, 20]),
]

# TODO: ID professor, name Professor, ENTRADA NUCLEO, id Nucleo
nucleo_restriction_list = [
    (19, "Juliano Lopes de Oliveira", "dez./2022", [1]),
    (20, "Alessandro Cruvinel Machado de Araújo", "dez./2022", [1]),
    (16, "Adailton Ferreira de Araújo", "nov./2023", [1]),
    (13, "William Divino Ferreira", "dez./2022", [1]),
    (18, "Leonardo Antonio Alves", "nov./2023", [2]),
    (17, "Hugo Nascimento", "dez./2022", [2])
]

 
def parse_date(date_str):
    month_mapping = {
        'jan.': '01',
        'fev.': '02',
        'mar.': '03',
        'abr.': '04',
        'mai.': '05',
        'jun.': '06',
        'jul.': '07',
        'ago.': '08',
        'set.': '09',
        'out.': '10',
        'nov.': '11',
        'dez.': '12'
    }
    month_str, year_str = date_str.split('/')
    month_number_str = month_mapping.get(month_str.lower())
    if not month_number_str:
        raise ValueError(f"Invalid month: {month_str}")
    return datetime.strptime(f"{month_number_str}/{year_str}", '%m/%Y')

# def get_nucleo_restrictions():
#     restrictions = {}
#     for teacher_id, _, entry_date, nucleo_ids in nucleo_restriction_list:
#         restrictions[teacher_id] = {
#             'entry_date': parse_date(entry_date),
#             'nucleo_ids': set(nucleo_ids)
#         }
#     return restrictions

# nucleo_restrictions = get_nucleo_restrictions()
# print(nucleo_restrictions)


@constraint_provider
def define_constraints(constraint_factory):
    constraints = []  
    constraints.extend([
        # Restrições de conflitos de interesse de professores
        ## Garante que nenhum professor ensine a mesma disciplina mais de uma vez no mesmo ano.
        constraint_factory.for_each(Lesson)
                         .join(Lesson,
                               Joiners.equal(lambda lesson: lesson.subject),
                               Joiners.equal(lambda lesson: lesson.teacher))
                         .penalize("Same teacher for the same subject", HardSoftScore.ofSoft(10)),

        # Restrição de última aula ministrada
        ## Garante que professores que ministraram a disciplina na última vez que foi oferecida não a ministrem 
        constraint_factory.for_each(Lesson)
                         .join(Lesson,
                               Joiners.equal(lambda lesson: lesson.subject),
                               Joiners.equal(lambda lesson: lesson.teacher),
                               Joiners.filtering(lambda l1, l2: l1.year == l2.year - 1))
                         .penalize("Teacher taught last time", HardSoftScore.ofSoft(10)),

        # Restrição de últimas duas aulas ministradas
        ## Garante que professores que ministraram a disciplina nas duas últimas vezes que foi oferecida não a ministrem novamente.
        constraint_factory.for_each(Lesson)
                         .join(Lesson,
                               Joiners.equal(lambda lesson: lesson.subject),
                               Joiners.equal(lambda lesson: lesson.teacher),
                               Joiners.filtering(lambda l1, l2: l1.year == l2.year - 2))
                         .penalize("Teacher taught the last two times", HardSoftScore.ofSoft(10)),

    ])
    # Restrições de professores válidos para a disciplina
    ## Garante que apenas professores permitidos podem ministrar certas disciplinas.
    for possibility in possibilite_lesson_list:
        subject_id, subject_code, allowed_teacher_ids = possibility
        constraints.append(
            constraint_factory.for_each(Lesson)
                             .filter(lambda lesson: lesson.subject.id == subject_id)
                             .filter(lambda lesson: lesson.teacher is not None)
                             .filter(lambda lesson: lesson.teacher.id not in allowed_teacher_ids)
                             .penalize("Invalid teacher for subject {}".format(subject_code), HardSoftScore.ONE_HARD)
        )

    # Restrição de conflito de interesse de núcleo
    # constraints.append(conflicting_nucleo_interest(constraint_factory, nucleo_restriction_list))
    
    return constraints

# Restrições de conflito de interesse de núcleo
## Garante que professores dentro do mesmo núcleo que já ministraram a disciplina no último ano não a ministrem novamente.
def conflicting_nucleo_interest(constraint_factory: ConstraintFactory, nucleo_restriction_list):
    added_constraints = set()  
    for teacher1_id, _, _, nucleo1_ids in nucleo_restriction_list:
        for teacher2_id, _, _, nucleo2_ids in nucleo_restriction_list:
            if teacher1_id != teacher2_id:
                common_nucleos = set(nucleo1_ids) & set(nucleo2_ids)
                if common_nucleos and len(common_nucleos) > 0:
                    constraint_id = f"Conflicting nucleo interest ({teacher1_id}, {teacher2_id})"
                    if constraint_id not in added_constraints:
                        return constraint_factory.for_each(Lesson)\
                                             .join(Lesson,
                                                   Joiners.equal(lambda lesson: lesson.subject),
                                                   Joiners.equal(lambda lesson: lesson.teacher),
                                                   Joiners.filtering(lambda l1, l2:
                                                                     l1.teacher.id == teacher1_id and
                                                                     l2.teacher.id == teacher2_id and
                                                                     l1.year == l2.year - 1))\
                                             .penalize(constraint_id, HardSoftScore.ONE_HARD)
                    added_constraints.add(constraint_id)

    return None 


