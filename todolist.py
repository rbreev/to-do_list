from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def today_tasks():
    list_tasks = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    print("Today " + datetime.today().strftime("%d %b") + ":")
    if len(list_tasks) == 0:
        print("Nothing to do!")
    else:
        for i in range(len(list_tasks)):
            print(f'{i+1}. {list_tasks[i].task}')
    print()
    menu()


def add_task():
    print('Enter task')
    new_task = input()
    print('Enter deadline')
    n_year, n_month, n_day = input().split("-")
    new_deadline = datetime(int(n_year), int(n_month), int(n_day))
    new_row = Table(task=new_task, deadline=new_deadline)
    session.add(new_row)
    session.commit()
    menu()


def del_task():
    list_tasks = session.query(Table.id,Table.task, Table.deadline).order_by(Table.deadline).all()
    print('Chose the number of the task you want to delete:')
    for i in range(len(list_tasks)):
        print(f'{i + 1}. {list_tasks[i][1]}. {list_tasks[i][2].strftime("%d %b")}')
    del_number = int(input()) - 1
    del_row = list_tasks[del_number]
    session.query(Table).filter(Table.id == del_row[0]).delete()
    session.commit()
    print("The task has been deleted!")
    menu()


def all_tasks():
    list_tasks = session.query(Table.task, Table.deadline).order_by(Table.deadline).all()
    print('All tasks:')
    for i in range(len(list_tasks)):
        print(f'{i + 1}. {list_tasks[i][0]}. {list_tasks[i][1].strftime("%d %b")}')
    print()
    menu()


def week_tasks():
    for i in range(7):
        date = datetime.today().date() + timedelta(days=i)
        list_tasks = session.query(Table).filter(Table.deadline == date).all()
        print(date.strftime("%A %d %b") + ":")
        if len(list_tasks) == 0:
            print("Nothing to do!")
        else:
            for j in range(len(list_tasks)):
                print(f'{j+1}. {list_tasks[j].task}')
        print()
    menu()


def missed_tasks():
    list_tasks = session.query(Table.task, Table.deadline).filter(Table.deadline < datetime.today()).all()
    print("Missed tasks:")
    if len(list_tasks) == 0:
        print("Nothing is missed!")
    else:
        for i in range(len(list_tasks)):
            print(f'{i + 1}. {list_tasks[i][0]}. {list_tasks[i][1].strftime("%d %b")}')
    print()
    menu()


def menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    action = input()
    if action == "1":
        today_tasks()
    elif action == "2":
        week_tasks()
    elif action == "3":
        all_tasks()
    elif action == "4":
        missed_tasks()
    elif action == "5":
        add_task()
    elif action == "6":
        del_task()
    elif action == "0":
        print('Bye!')
        exit()


menu()
