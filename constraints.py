from domain import Lesson
from optapy import constraint_provider
from optapy.constraint import Joiners, ConstraintFactory
from optapy.score import HardSoftScore


@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        # Hard constraints
        teacher_interest_constraint(constraint_factory),
        teacher_3_consecutive_times(constraint_factory),
        # Soft constraints
        teacher_conflict_1_constraint(constraint_factory),
        teacher_conflict_2_constraint(constraint_factory),
        teacher_conflict_3_constraint(constraint_factory),
    ]


def teacher_interest_constraint(constraint_factory):
    # A disciplina só pode ser ministrada por professores interessados nela.
    return (
        constraint_factory.for_each(Lesson)
        .filter(
            lambda lesson: lesson.teacher.id
            not in lesson.subject.interested_teacher_ids
        )
        .penalize("Professor não interessado na disciplina", HardSoftScore.ONE_HARD)
    )

def teacher_3_consecutive_times(constraint_factory):
    # Penaliza professor que ministrou a disciplina nas últimas 3 vezes que foi ofertada
    return (
        constraint_factory.for_each(Lesson)
        .filter(lambda lesson: did_teach_last_3_times(lesson))
        .penalize(
            "Ministrou a disciplina nas últimas 3 vezes que foi ofertada",
            HardSoftScore.ONE_HARD,
        )
    )


def teacher_conflict_1_constraint(constraint_factory):
    # Recompensa o professor que ministrou a disciplina na última vez que foi ofertada e não a ministrou na penúltima oferta.
    return (
        constraint_factory.for_each(Lesson)
        .filter(lambda lesson: did_teach_last_time_but_not_penultimate(lesson))
        .reward(
            "Ministrou a disciplina na última vez e não na penúltima",
            HardSoftScore.ofSoft(15),
        )
    )


def teacher_conflict_2_constraint(constraint_factory):
    # Recompensa o professor que ministrou a disciplina na última e penúltima vezes que foi ofertada
    return (
        constraint_factory.for_each(Lesson)
        .filter(lambda lesson: did_teach_last_and_penultimate_time(lesson))
        .reward(
            "Ministrou a disciplina na última e na penúltima vez",
            HardSoftScore.ofSoft(10),
        )
    )

def teacher_conflict_3_constraint(constraint_factory):
    # Recompensa para o professor que nunca ministrou a disciplina anteriormente.
    return (
        constraint_factory.for_each(Lesson)
        .filter(lambda lesson: is_new_teacher_for_subject(lesson))
        .reward("Professor nunca ministrou a disciplina", HardSoftScore.ofSoft(5))
    )


def did_teach_last_time_but_not_penultimate(lesson):
    # Verifica se o professor ministrou a disciplina na última vez que foi ofertada e não ministrou na penúltima vez.
    subject_history = lesson.subject.historical_teacher_ids
    if len(subject_history) < 2:
        return False
    last_teacher = subject_history[-1]
    penultimate_teacher = subject_history[-2]
    return (
        lesson.teacher.id == last_teacher and lesson.teacher.id != penultimate_teacher
    )


def did_teach_last_and_penultimate_time(lesson):
    # Verifica se o professor ministrou a disciplina na última e penúltima vezes que foi ofertada
    subject_history = lesson.subject.historical_teacher_ids
    if len(subject_history) < 2:
        return False
    last_teacher = subject_history[-1]
    penultimate_teacher = subject_history[-2]
    return (
        lesson.teacher.id == last_teacher and lesson.teacher.id == penultimate_teacher
    )

def did_teach_last_3_times(lesson):
    # Verifica se o professor ministrou a disciplina na última e penúltima vezes que foi ofertada
    subject_history = lesson.subject.historical_teacher_ids
    if len(subject_history) < 3:
        return False
    last_teacher = subject_history[-1]
    penultimate_teacher = subject_history[-2]
    antepenultimate_teacher = subject_history[-3]
    return (
        lesson.teacher.id == last_teacher and lesson.teacher.id == penultimate_teacher and lesson.teacher.id == antepenultimate_teacher
    )

def is_new_teacher_for_subject(lesson):
    # Verifica se o professor nunca ministrou a disciplina anteriormente.
    return lesson.teacher.id not in lesson.subject.historical_teacher_ids