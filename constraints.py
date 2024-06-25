from domain import Lesson
from optapy import constraint_provider
from optapy.constraint import Joiners, ConstraintFactory
from optapy.score import HardSoftScore


@constraint_provider
def define_constraints(constraint_factory: ConstraintFactory):
    return [
        # Hard constraints
        teacher_interest_constraint(constraint_factory),
        teacher_3_consecutive_times_constraint(constraint_factory),
        # Soft constraints
        teacher_conflict_1_constraint(constraint_factory),
        teacher_conflict_2_constraint(constraint_factory),
        teacher_conflict_3_constraint(constraint_factory),
        teacher_conflict_4_constraint(constraint_factory),
    ]


# A disciplina só pode ser ministrada por professores interessados nela.
def teacher_interest_constraint(constraint_factory):
    return (
        constraint_factory.for_each(Lesson)
        .filter(
            lambda lesson: lesson.teacher.id
            not in lesson.subject.interested_teacher_ids
        )
        .penalize("Professor não interessado na disciplina", HardSoftScore.ONE_HARD)
    )


# Penaliza professor que ministrou a disciplina nas últimas 3 vezes que foi ofertada
def teacher_3_consecutive_times_constraint(constraint_factory):
    return (
        constraint_factory.for_each(Lesson)
        .filter(lambda lesson: did_teach_last_3_times(lesson))
        .penalize(
            "Ministrou a disciplina nas últimas 3 vezes que foi ofertada",
            HardSoftScore.ONE_HARD,
        )
    )


# Recompensa o professor que ministrou a disciplina na última vez que foi ofertada e não a ministrou na penúltima oferta.
def teacher_conflict_1_constraint(constraint_factory):
    return (
        constraint_factory.for_each(Lesson)
        .filter(lambda lesson: did_teach_last_time_but_not_penultimate(lesson))
        .reward(
            "Ministrou a disciplina na última vez e não na penúltima",
            HardSoftScore.ofSoft(20),
        )
    )


# Recompensa o professor que ministrou a disciplina na última e penúltima vezes que foi ofertada
def teacher_conflict_2_constraint(constraint_factory):
    return (
        constraint_factory.for_each(Lesson)
        .filter(lambda lesson: did_teach_last_and_penultimate_time(lesson))
        .reward(
            "Ministrou a disciplina na última e na penúltima vez",
            HardSoftScore.ofSoft(15),
        )
    )


# Recompensa o professor que nunca ministrou a disciplina anteriormente.
def teacher_conflict_3_constraint(constraint_factory):
    return (
        constraint_factory.for_each(Lesson)
        .filter(lambda lesson: is_new_teacher_for_subject(lesson))
        .reward("Professor nunca ministrou a disciplina", HardSoftScore.ofSoft(10))
    )


# Recompensa o professor que ministrou a disciplina há mais tempo dentre a lista de interessados.
def teacher_conflict_4_constraint(constraint_factory):
    return (
        constraint_factory.for_each(Lesson)
        .filter(lambda lesson: last_teacher_to_teach(lesson) is not None)
        .reward(
            "Professor que ministrou a disciplina a mais tempo",
            HardSoftScore.ofSoft(5),
        )
    )


# Verifica se o professor ministrou a disciplina na última vez que foi ofertada e não ministrou na penúltima vez.
def did_teach_last_time_but_not_penultimate(lesson):
    subject_history = lesson.subject.historical_teacher_ids
    if len(subject_history) < 2:
        return False
    last_teacher = subject_history[-1]
    penultimate_teacher = subject_history[-2]
    return (
        lesson.teacher.id == last_teacher and lesson.teacher.id != penultimate_teacher
    )


# Verifica se o professor ministrou a disciplina na última e penúltima vezes que foi ofertada
def did_teach_last_and_penultimate_time(lesson):
    subject_history = lesson.subject.historical_teacher_ids
    if len(subject_history) < 2:
        return False
    last_teacher = subject_history[-1]
    penultimate_teacher = subject_history[-2]
    return (
        lesson.teacher.id == last_teacher and lesson.teacher.id == penultimate_teacher
    )


# Verifica se o professor ministrou a disciplina nas 3 últimas vezes que foi ofertada
def did_teach_last_3_times(lesson):
    subject_history = lesson.subject.historical_teacher_ids
    if len(subject_history) < 3:
        return False
    last_teacher = subject_history[-1]
    penultimate_teacher = subject_history[-2]
    antepenultimate_teacher = subject_history[-3]
    return (
        lesson.teacher.id == last_teacher
        and lesson.teacher.id == penultimate_teacher
        and lesson.teacher.id == antepenultimate_teacher
    )


# Verifica se o professor nunca ministrou a disciplina anteriormente.
def is_new_teacher_for_subject(lesson):
    return lesson.teacher.id not in lesson.subject.historical_teacher_ids


# Verifica o professor que ministrou a disciplina a mais tempo dentre a lista de interessados.
def last_teacher_to_teach(lesson):
    subject_history = lesson.subject.historical_teacher_ids
    subject_interested = lesson.subject.interested_teacher_ids

    interested_teacher_positions = {}

    for i, teacher_id in enumerate(subject_history):
        if teacher_id in subject_interested:
            if teacher_id not in interested_teacher_positions:
                interested_teacher_positions[teacher_id] = i

    if not interested_teacher_positions:
        return None

    last_teacher_id = min(
        interested_teacher_positions, key=interested_teacher_positions.get
    )

    return last_teacher_id
