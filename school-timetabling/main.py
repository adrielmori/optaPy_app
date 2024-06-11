from functools import reduce

from optapy import solver_factory_create
from optapy.types import SolverConfig, Duration
from domain import TimeTable, Lesson, generate_problem
from constraints import define_constraints


def print_timetable(timetable: TimeTable):
    lesson_list = timetable.lesson_list
    lesson_list_2024 = list(filter(lambda the_lesson: the_lesson.year == 2024, lesson_list))

    print("|-------------------|-------------------|")
    print("| Subject           | Teacher           |")
    print("|-------------------|-------------------|")
    for lesson in lesson_list_2024:
        out = "| " + "{:<15}".format(lesson.subject.name)[0:15] + " | "
        out += "{:<15}".format(lesson.teacher.name)[0:15] + " | "
        print(out)
    print("|-------------------|-------------------|")

    unassigned_lessons = list(
        filter(lambda unassigned_lesson: unassigned_lesson.year == 2024 and unassigned_lesson.teacher is None,
               lesson_list))
    if len(unassigned_lessons) > 0:
        print()
        print("Unassigned lessons")
        for lesson in unassigned_lessons:
            print(" " + lesson.subject.name + " - No teacher assigned")



solver_config = SolverConfig().withEntityClasses(Lesson) \
    .withSolutionClass(TimeTable) \
    .withConstraintProviderClass(define_constraints) \
    .withTerminationSpentLimit(Duration.ofSeconds(30))

solver = solver_factory_create(solver_config).buildSolver()

print(generate_problem())

solution = solver.solve(generate_problem())

print("solution", solution)

print_timetable(solution)