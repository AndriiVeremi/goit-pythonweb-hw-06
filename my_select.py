from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

from conf.db import SessionLocal
from entity.models import Student, Grade, Subject, Teacher, Group


# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_01(session: Session):
    query = (
        select(Student, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(query).all()


# 2. Знайти студента із найвищим середнім балом з певного предмета
def select_02(session: Session, subject_id: int):
    query = (
        select(Student, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .where(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    return session.execute(query).first()


# 3. Знайти середній бал у групах з певного предмета
def select_03(session: Session, subject_id: int):
    query = (
        select(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .select_from(Group)  # Вказуємо початкову таблицю
        .join(Student)  # З'єднуємо з Student
        .join(Grade)  # З'єднуємо з Grade
        .where(Grade.subject_id == subject_id)
        .group_by(Group.id)
    )
    return session.execute(query).all()


# 4. Знайти середній бал на потоці (по всій таблиці оцінок)
def select_04(session: Session):
    query = select(func.avg(Grade.grade).label("avg_grade"))
    return session.execute(query).scalar()


# 5. Знайти які курси читає певний викладач
def select_05(session: Session, teacher_id: int):
    query = (
        select(Subject)
        .where(Subject.teacher_id == teacher_id)
    )
    return session.execute(query).all()


# 6. Знайти список студентів у певній групі
def select_06(session: Session, group_id: int):
    query = (
        select(Student)
        .where(Student.group_id == group_id)
    )
    return session.execute(query).all()


# 7. Знайти оцінки студентів у окремій групі з певного предмета
def select_07(session: Session, group_id: int, subject_id: int):
    query = (
        select(Student.full_name, Grade.grade, Grade.date_received)
        .join(Grade)
        .where(Grade.subject_id == subject_id, Student.group_id == group_id)
    )
    return session.execute(query).all()


# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_08(session: Session, teacher_id: int):
    query = (
        select(func.avg(Grade.grade).label("avg_grade"))
        .select_from(Subject)  # Додаємо для уникнення неоднозначності
        .join(Grade)
        .where(Subject.teacher_id == teacher_id)
    )
    return session.execute(query).scalar()


# 9. Знайти список курсів, які відвідує певний студент
def select_09(session: Session, student_id: int):
    query = (
        select(Subject)
        .join(Grade)
        .where(Grade.student_id == student_id)
        .distinct()
    )
    return session.execute(query).all()


# 10. Список курсів, які певному студенту читає певний викладач
def select_10(session: Session, student_id: int, teacher_id: int):
    query = (
        select(Subject)
        .join(Grade)
        .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
    )
    return session.execute(query).all()

# 11. Середній бал, який певний викладач ставить певному студентові
def select_11(session: Session, student_id: int, teacher_id: int):
    query = (
        select(func.avg(Grade.grade).label("avg_grade"))
        .select_from(Grade)
        .join(Subject)
        .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
    )
    return session.execute(query).scalar()

# 12. Оцінки студентів у певній групі з певного предмета на останньому занятті
def select_12(session: Session, group_id: int, subject_id: int):
    subquery = (
        select(func.max(Grade.date_received).label("max_date"))
        .join(Student)
        .where(Grade.subject_id == subject_id, Student.group_id == group_id)
        .scalar_subquery()
    )
    query = (
        select(Student.full_name, Grade.grade, Grade.date_received)
        .join(Grade)
        .where(
            Grade.subject_id == subject_id,
            Student.group_id == group_id,
            Grade.date_received == subquery
        )
    )
    return session.execute(query).all()


if __name__ == "__main__":
    session: Session = SessionLocal()

    try:
        # Приклади викликів функцій з тестовими параметрами
        result_01 = select_01(session)
        result_02 = select_02(session, 1)
        result_03 = select_03(session, 1)
        result_04 = select_04(session)
        result_05 = select_05(session, 1)
        result_06 = select_06(session, 1)
        result_07 = select_07(session, 1, 1)
        result_08 = select_08(session, 1)
        result_09 = select_09(session, 1)
        result_10 = select_10(session, 1, 1)
        result_11 = select_11(session, 1, 1)  # Новий запит
        result_12 = select_12(session, 1, 1)  # Новий запит

        # Форматований вивід
        print("1. 5 студентів з найбільшим середнім балом:")
        for student, avg_grade in result_01:
            print(f"  {student.full_name}: {avg_grade:.2f}")

        print("2. Студент з найвищим балом з предмета:")
        if result_02:
            print(f"  {result_02[0].full_name}: {result_02[1]:.2f}")

        print("3. Середній бал у групах з предмета:")
        for group_name, avg_grade in result_03:
            print(f"  {group_name}: {avg_grade:.2f}")

        print(f"4. Середній бал на потоці: {result_04:.2f}")

        print("5. Курси викладача:")
        for subject, in result_05:
            print(f"  {subject.name}")

        print("6. Студенти у групі:")
        for student, in result_06:
            print(f"  {student.full_name}")

        print("7. Оцінки у групі з предмета:")
        for name, grade, date in result_07:
            print(f"  {name}: {grade} ({date})")

        print(f"8. Середній бал викладача: {result_08:.2f}")

        print("9. Курси студента:")
        for subject, in result_09:
            print(f"  {subject.name}")

        print("10. Курси від викладача студенту:")
        for subject, in result_10:
            print(f"  {subject.name}")

        print(f"11. Середній бал від викладача студенту: {result_11:.2f}")

        print("12. Оцінки на останньому занятті:")
        for name, grade, date in result_12:
            print(f"  {name}: {grade} ({date})")

    finally:
        session.close()