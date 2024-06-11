from optapy import constraint_provider
from optapy.score import HardSoftScore
from optapy.constraint import ConstraintFactory, Joiners
from domain import Lesson, Interest, Subjective, Teacher
from datetime import datetime, date, timedelta


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

# Type annotation not needed, but allows you to get autocompletion
@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        # Hard constraints
        teacher_conflict(constraint_factory)
        teacher_repeated(constraint_factory)
    ]

# Para resolver anomalia do tipo Conflito (disciplina com mais de um docente interessado), o facilitador deve indicar o(s) docente(s) que permanece(m) na disciplina para cada conflito, usando os seguintes critérios, nesta ordem, para indicação:
#   1. Docente que ministrou a disciplina na última vez em que foi ofertada e não a ministrou na penúltima oferta
def teacher_conflict(constraint_factory: ConstraintFactory):
    # A teacher who taught the subject the last time it was offered and did not teach it the penultimate offer.
    return constraint_factory \
        .from_(Lesson) \
        .join(Lesson,
              # ... in the same subject ...
              Joiners.equal(lambda lesson: lesson.subject),
              # ... by the same teacher ...
              Joiners.equal(lambda lesson: lesson.teacher),
              # ... and the teacher did not teach it the penultimate offer
              Joiners.filtering(lambda lesson, other_lesson: 
                                lesson.year == other_lesson.year - 1 and 
                                lesson.teacher != other_lesson.teacher)
              ) \
        .if_exists(Interest,
                   # ... with the same teacher and subject ...
                   Joiners.equal(lambda lesson: lesson.teacher, lambda interest: interest.teacher),
                   Joiners.equal(lambda lesson: lesson.subject, lambda interest: interest.subjective)
                   ) \
        .penalize("Teacher conflict", HardSoftScore.ONE_HARD)


#   2.Docente que ministrou a disciplina nas duas últimas vezes em que foi ofertada.
def teacher_repeated(constraint_factory: ConstraintFactory):
    # A teacher who taught the subject the last two times it was offered.
    return constraint_factory \
        .from_(Lesson) \
        .join(Lesson,
              # ... in the same subject ...
              Joiners.equal(lambda lesson: lesson.subject),
              # ... by the same teacher ...
              Joiners.equal(lambda lesson: lesson.teacher),
              # ... and the teacher taught it the last time it was offered
              Joiners.filtering(lambda lesson, other_lesson: 
                                lesson.year == other_lesson.year - 1)
              ) \
        .join(Lesson,
              # ... in the same subject ...
              Joiners.equal(lambda lesson, other_lesson: lesson.subject),
              # ... by the same teacher ...
              Joiners.equal(lambda lesson, other_lesson: lesson.teacher),
              # ... and the teacher taught it the penultimate time it was offered
              Joiners.filtering(lambda lesson, other_lesson, yet_another_lesson: 
                                lesson.year == yet_another_lesson.year - 2)
              ) \
        .penalize("Teacher repeated", HardSoftScore.ONE_HARD)



