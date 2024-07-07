from flask import Flask, request, jsonify
from domain import Lesson, TimeTable, generate_problem
from constraints import define_constraints
import optapy.config
from optapy.types import Duration
from optapy import solver_factory_create

from utils.utils import print_timetable, timetable_to_json

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solveRequest():
    solver_config = (
        optapy.config.solver.SolverConfig()
        .withEntityClasses(Lesson)
        .withSolutionClass(TimeTable)
        .withConstraintProviderClass(define_constraints)
        .withTerminationSpentLimit(Duration.ofSeconds(30))
    )

    data = request.get_json()

    print(generate_problem(data))

    solution = solver_factory_create(solver_config).buildSolver().solve(generate_problem(data))

    print_timetable(solution.lesson_list)

    return jsonify(timetable_to_json(solution.lesson_list, solution.score))

if __name__ == '__main__':
    app.run(debug=True)