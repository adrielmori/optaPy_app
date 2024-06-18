from optapy import constraint_provider
from optapy.score import HardSoftScore
from optapy.constraint import ConstraintFactory, Joiners

from optapy import constraint_provider, get_class
from optapy import constraint_provider
from optapy.constraint import ConstraintFactory
from optapy.score import HardSoftScore

from datetime import datetime, date, timedelta

from utils import *
from domain import Lesson, Interest, Subjective, Teacher

# Obtenção das classes
# LessonClass = get_class(Lesson)
# TeacherClass = get_class(Teacher)
# SubjectiveClass = get_class(Subjective)
# InterestClass = get_class(Interest)

interest_lesson_list = [
    Interest(Subjective(1, "INF0291"), Teacher(1, "Plínio de Sá Leitão Júnior")),
    Interest(Subjective(1, "INF0291"), Teacher(2, "Reinaldo de Souza Júnior")),
    Interest(Subjective(1, "INF0291"), Teacher(3, "Fábio Nogueira de Lucena")),
    Interest(Subjective(2, "INF0292"), Teacher(4, "Taciana Novo Kudo")),
    Interest(Subjective(2, "INF0292"), Teacher(5, "Renata Dutra Braga")),
    Interest(Subjective(3, "INF0287"), Teacher(6, "Ana Claudia Bastos Loureiro Monção")),
    Interest(Subjective(3, "INF0287"), Teacher(7, "Sofia Larissa da Costa Paiva")),
    Interest(Subjective(3, "INF0287"), Teacher(8, "Leonardo Andrade Ribeiro")),
    Interest(Subjective(4, "INF0018"), Teacher(9, "Jacson Rodrigues Barbosa")),
    Interest(Subjective(4, "INF0018"), Teacher(7, "Sofia Larissa da Costa Paiva")),
    Interest(Subjective(5, "INF0283"), Teacher(7, "Sofia Larissa da Costa Paiva")),
    Interest(Subjective(5, "INF0283"), Teacher(6, "Ana Claudia Bastos Loureiro Monção")),
    Interest(Subjective(5, "INF0283"), Teacher(10, "Renato Bulcão")),
    Interest(Subjective(6, "INF0294"), Teacher(11, "Eliomar Araújo de Lima")),
    Interest(Subjective(6, "INF0294"), Teacher(12, "Evellin Cardoso")),
    Interest(Subjective(7, "INF0056"), Teacher(2, "Reinaldo de Souza Júnior")),
    Interest(Subjective(7, "INF0056"), Teacher(1, "Plínio de Sá Leitão Júnior")),
    Interest(Subjective(8, "INF0299"), Teacher(10, "Renato Bulcão")),
    Interest(Subjective(8, "INF0299"), Teacher(6, "Ana Claudia Bastos Loureiro Monção")),
    Interest(Subjective(8, "INF0299"), Teacher(7, "Sofia Larissa da Costa Paiva")),
    Interest(Subjective(9, "INF0285"), Teacher(13, "William Divino Ferreira")),
    Interest(Subjective(9, "INF0285"), Teacher(14, "Rubens de Castro Pereira")),
    Interest(Subjective(10, "INF0293"), Teacher(15, "Edison Andrade Martins Morais")),
    Interest(Subjective(10, "INF0293"), Teacher(4, "Taciana Novo Kudo")),
    Interest(Subjective(11, "INF0300"), Teacher(16, "Adailton Ferreira de Araújo")),
    Interest(Subjective(11, "INF0300"), Teacher(13, "William Divino Ferreira")),
    Interest(Subjective(12, "INF0284"), Teacher(17, "Hugo Nascimento")),
    Interest(Subjective(12, "INF0284"), Teacher(18, "Leonardo Antonio Alves")),
    Interest(Subjective(13, "INF0288"), Teacher(19, "Juliano Lopes de Oliveira")),
    Interest(Subjective(13, "INF0288"), Teacher(20, "Alessandro Cruvinel Machado de Araújo")),
]

# Obtenção das classes
LessonClass = get_class(Lesson)
TeacherClass = get_class(Teacher)
SubjectiveClass = get_class(Subjective)
InterestClass = get_class(Interest)

# Define the constraint provider
@constraint_provider
def define_constraints(constraint_factory):
    return [
        conflicting_teacher_interests(constraint_factory),
        # teacher_taught_last_time(constraint_factory),
        # teacher_taught_last_two_times(constraint_factory),
    ]

# def teacher_taught_last_time(constraint_factory):
#     # Restriction: Teachers from the interest list who taught the subject last time and did not teach it the time before

#     last_year = 2023
#     penultimate_year = 2022

#     def get_teacher_for_subject(year):
#         return constraint_factory.from_(Lesson) \
#             .filter(lambda lesson: lesson.year == year) \
#             .group_by(lambda lesson: lesson.subjective,
#                       lambda lesson: lesson.teacher) \
#             .if_exists(lambda key, group: group.single())

#     last_year_teachers = get_teacher_for_subject(last_year)
#     penultimate_year_teachers = get_teacher_for_subject(penultimate_year)

#     return constraint_factory.from_(LessonClass) \
#         .filter(lambda la: la.teacher is not None and \
#                 la.lesson.subjective in last_year_teachers and \
#                 last_year_teachers[la.lesson.subjective] == la.teacher and \
#                 (la.lesson.subjective not in penultimate_year_teachers or \
#                  penultimate_year_teachers[la.lesson.subjective] != la.teacher)) \
#         .penalize("Teacher taught last time", HardSoftScore.ONE_HARD)

# def teacher_taught_last_two_times(constraint_factory):
#     # Restriction: Teachers from the interest list who taught the subject in the last two offerings

#     last_year = 2023
#     penultimate_year = 2022

#     def get_teacher_for_subject(year):
#         return constraint_factory.from_(Lesson) \
#             .filter(lambda lesson: lesson.year == year) \
#             .group_by(lambda lesson: lesson.subjective,
#                       lambda lesson: lesson.teacher) \
#             .if_exists(lambda key, group: group.single())

#     last_year_teachers = get_teacher_for_subject(last_year)
#     penultimate_year_teachers = get_teacher_for_subject(penultimate_year)

#     return constraint_factory.from_(LessonClass) \
#         .filter(lambda la: la.teacher is not None and \
#                 la.lesson.subjective in last_year_teachers and \
#                 la.lesson.subjective in penultimate_year_teachers and \
#                 last_year_teachers[la.lesson.subjective] == la.teacher and \
#                 penultimate_year_teachers[la.lesson.subjective] == la.teacher) \
#         .penalize("Teacher taught last two times", HardSoftScore.ONE_HARD)

def conflicting_teacher_interests(constraint_factory):
    # Restriction: Teachers from the interest list wanting to teach the same subject
    return constraint_factory.from_(LessonClass) \
        .filter(lambda la: la.teacher is not None) \
        .join(Interest,
              Joiners.equal(lambda la: la.lesson.subjective, lambda interest: interest.subjective),
              Joiners.equal(lambda la: la.teacher, lambda interest: interest.teacher)) \
        .penalize("Conflicting teacher interests", HardSoftScore.ONE_HARD)