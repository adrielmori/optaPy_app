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

nucleo_list = [
    Nucleo(1, "2.1 - Núcleo de Fundamentos de Sistemas e Software"),
    Nucleo(2, "2.2 - Núcleo de Aplicações e Tecnologias de Sistemas e Software")
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

def get_nucleo_restrictions():
    restrictions = {}
    for teacher_id, _, entry_date, nucleo_ids in nucleo_restriction_list:
        restrictions[teacher_id] = {
            'entry_date': parse_date(entry_date),
            'nucleo_ids': set(nucleo_ids)
        }
    return restrictions

nucleo_restrictions = get_nucleo_restrictions()
print(nucleo_restrictions)

def has_conflicting_nucleo_interest(l1, l2):
    l1_restrictions = nucleo_restrictions.get(l1.teacher.id)
    l2_restrictions = nucleo_restrictions.get(l2.teacher.id)
    if l1_restrictions and l2_restrictions:
        shared_nucleos = l1_restrictions['nucleo_ids'] & l2_restrictions['nucleo_ids']
        if shared_nucleos and l1.year == l2.year - 1:
            return True
    return False

@constraint_provider
def define_constraints(constraint_factory):
    constraints = []
    constraints.extend([
        # Restrições de conflitos de interesse de professores
        ## Garante que nenhum professor ensine a mesma disciplina mais de uma vez no mesmo ano.
        constraint_factory.from_(Lesson)
                         .join(Lesson,
                               Joiners.equal(lambda lesson: lesson.subject),
                               Joiners.equal(lambda lesson: lesson.teacher))
                         .penalize("Same teacher for the same subject", HardSoftScore.ONE_HARD),

        # Restrição de última aula ministrada
        ## Garante que professores que ministraram a disciplina na última vez que foi oferecida não a ministrem 
        constraint_factory.from_(Lesson)
                         .join(Lesson,
                               Joiners.equal(lambda lesson: lesson.subject),
                               Joiners.equal(lambda lesson: lesson.teacher),
                               Joiners.filtering(lambda l1, l2: l1.year == l2.year - 1))
                         .penalize("Teacher taught last time", HardSoftScore.ONE_HARD),

        # Restrição de últimas duas aulas ministradas
        ## Garante que professores que ministraram a disciplina nas duas últimas vezes que foi oferecida não a ministrem novamente.
        constraint_factory.from_(Lesson)
                         .join(Lesson,
                               Joiners.equal(lambda lesson: lesson.subject),
                               Joiners.equal(lambda lesson: lesson.teacher),
                               Joiners.filtering(lambda l1, l2: l1.year == l2.year - 2))
                         .penalize("Teacher taught the last two times", HardSoftScore.ONE_HARD),

        # Restrições de conflito de interesse de núcleo
        ## Garante que professores dentro do mesmo núcleo que já ministraram a disciplina no último ano não a ministrem novamente.
        # constraint_factory.from_(Lesson)
        #                  .join(Lesson,
        #                        Joiners.equal(lambda lesson: lesson.subject),
        #                        Joiners.equal(lambda lesson: lesson.teacher),
        #                        Joiners.filtering(lambda l1, l2: nucleo_restrictions.get(l1.teacher.id) and
        #                                                      nucleo_restrictions.get(l2.teacher.id) and
        #                                                      nucleo_restrictions[l1.teacher.id]['nucleo_ids'] &
        #                                                      nucleo_restrictions[l2.teacher.id]['nucleo_ids'] and
        #                                                      l1.year == l2.year - 1))
        #                  .penalize("Conflicting nucleo interest", HardSoftScore.ONE_HARD),
    ])

    # Restrições de professores válidos para a disciplina
    ## Garante que apenas professores permitidos podem ministrar certas disciplinas.
    for possibility in possibilite_lesson_list:
        subject_id, subject_code, allowed_teacher_ids = possibility
        constraints.append(
            constraint_factory.from_(Lesson)
                             .filter(lambda lesson: lesson.subject.id == subject_id)
                             .filter(lambda lesson: lesson.teacher is not None)
                             .filter(lambda lesson: lesson.teacher.id not in allowed_teacher_ids)
                             .penalize("Invalid teacher for subject {}".format(subject_code), HardSoftScore.ONE_HARD)
        )
    
    
    return constraints



