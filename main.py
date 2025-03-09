import argparse
from sqlalchemy.orm import Session
from conf.db import SessionLocal
from entity.models import Student, Grade, Subject, Teacher, Group

def create_teacher(session: Session, name: str, email: str = None, phone: str = None):
    first_name, last_name = name.split(" ", 1)
    teacher = Teacher(first_name=first_name, last_name=last_name, email=email or f"{first_name.lower()}@example.com", phone=phone)
    session.add(teacher)
    session.commit()
    print(f"Created teacher: {teacher.full_name}")

def create_group(session: Session, name: str):
    group = Group(name=name)
    session.add(group)
    session.commit()
    print(f"Created group: {group.name}")

def list_items(session: Session, model):
    items = session.query(model).all()
    for item in items:
        print(f"- {item.full_name if hasattr(item, 'full_name') else item.name} (ID: {item.id})")

def update_teacher(session: Session, id: int, name: str = None, email: str = None, phone: str = None):
    teacher = session.get(Teacher, id)
    if not teacher:
        print(f"Teacher with ID {id} not found")
        return
    if name:
        first_name, last_name = name.split(" ", 1)
        teacher.first_name = first_name
        teacher.last_name = last_name
    if email:
        teacher.email = email
    if phone:
        teacher.phone = phone
    session.commit()
    print(f"Updated teacher: {teacher.full_name}")

def remove_item(session: Session, model, id: int):
    item = session.get(model, id)
    if not item:
        print(f"{model.__name__} with ID {id} not found")
        return
    session.delete(item)
    session.commit()
    print(f"Removed {model.__name__}: {item.full_name if hasattr(item, 'full_name') else item.name}")

def main():
    parser = argparse.ArgumentParser(description="CLI for CRUD operations on database")
    parser.add_argument("-a", "--action", required=True, choices=["create", "list", "update", "remove"], help="Action to perform")
    parser.add_argument("-m", "--model", required=True, choices=["Teacher", "Group", "Student", "Subject", "Grade"], help="Model to operate on")
    parser.add_argument("--id", type=int, help="ID of the item")
    parser.add_argument("-n", "--name", help="Name (for Teacher: 'First Last', for Group: group name)")
    parser.add_argument("--email", help="Email (for Teacher)")
    parser.add_argument("--phone", help="Phone (for Teacher)")

    args = parser.parse_args()

    session: Session = SessionLocal()
    try:
        model_map = {
            "Teacher": Teacher,
            "Group": Group,
            "Student": Student,
            "Subject": Subject,
            "Grade": Grade
        }
        model = model_map[args.model]

        if args.action == "create":
            if args.model == "Teacher":
                create_teacher(session, args.name, args.email, args.phone)
            elif args.model == "Group":
                create_group(session, args.name)
        elif args.action == "list":
            list_items(session, model)

        elif args.action == "update":
            if args.model == "Teacher":
                update_teacher(session, args.id, args.name, args.email, args.phone)
        elif args.action == "remove":
            remove_item(session, model, args.id)

    finally:
        session.close()

if __name__ == "__main__":
    main()