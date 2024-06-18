def select_teacher(last_year_lesson, second_last_year_lesson, interest_list, subjective):
    # Regra 1: Docente que ministrou a disciplina na última vez e não na penúltima
    if last_year_lesson and second_last_year_lesson:
        if last_year_lesson.teacher != second_last_year_lesson.teacher:
            return last_year_lesson.teacher

    # Regra 2: Docente que ministrou a disciplina nas duas últimas vezes
    if last_year_lesson and second_last_year_lesson:
        if last_year_lesson.teacher == second_last_year_lesson.teacher:
            return last_year_lesson.teacher

    # Se nenhuma das regras acima se aplicar, escolher um professor interessado
    interested_teachers = [interest.teacher for interest in interest_list if interest.subjective == subjective]
    if interested_teachers:
        return interested_teachers[0]  # Escolhe o primeiro interessado como exemplo
    return None

def allocate_teachers(lesson_list, interest_list):
    lessons_2024 = [lesson for lesson in lesson_list if lesson.year == 2024]
    
    for lesson in lessons_2024:
        last_year_lesson = next((l for l in lesson_list if l.subjective == lesson.subjective and l.year == 2023), None)
        second_last_year_lesson = next((l for l in lesson_list if l.subjective == lesson.subjective and l.year == 2022), None)
        
        selected_teacher = select_teacher(last_year_lesson, second_last_year_lesson, interest_list, lesson.subjective)
        if selected_teacher:
            lesson.teacher = selected_teacher
        else:
            # Se não há informações sobre os anos anteriores, atribuir um professor interessado aleatoriamente
            interested_teachers = [interest.teacher for interest in interest_list if interest.subjective == lesson.subjective]
            if interested_teachers:
                lesson.teacher = interested_teachers[0]  # Escolhe o primeiro interessado como exemplo
