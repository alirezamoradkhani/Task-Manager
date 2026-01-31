import csv


def sort_tasks(goal_list: list):
    return sorted(goal_list, key=lambda task: task.imp, reverse=True)


def save_TDL_as_csv(task_list, to_do_list_name):
    file_of_TDL = open(
        file=f"ToDoList_{to_do_list_name}.csv",
        mode="w",
        encoding="UTF-8",
        newline=""
    )
    write_file_of_TDL = csv.writer(file_of_TDL)
    write_file_of_TDL.writerow(["title", "importance", "explain"])

    for task in task_list:
        write_file_of_TDL.writerow([task.title, task.imp, task.exp])

    file_of_TDL.close()


def create_task():
    new_task_title = input("enter the title of task: ")
    new_task = Task(new_task_title)

    command = input("do you want set importance? (y/n): ")
    if command == "y":
        new_task_imp = int(input("enter importance (0 to 5): "))
        if 0 <= new_task_imp <= 5:
            new_task.imp = new_task_imp
        else:
            print("invalid number, set to 0")

    command = input("do you want set explain? (y/n): ")
    if command == "y":
        new_task.exp = input("enter explain: ")

    return new_task


class Task:
    def __init__(self, title, imp: int = 0, exp=""):
        self.title = title
        self.imp = imp
        self.exp = exp

    def __str__(self):
        return f"{self.title} | importance: {self.imp} | explain: {self.exp}"


class TDL:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def info(self):
        if not self.tasks:
            print("ToDoList is empty")
            return

        row = 1
        for task in self.tasks:
            print(f"{row}. {task.title} | imp: {task.imp} | {task.exp}")
            row += 1

    def __str__(self):
        return f"{self.name} -> {[task.title for task in self.tasks]}"

    def add(self, task):
        self.tasks.append(task)
        self.tasks = sort_tasks(self.tasks)
        save_TDL_as_csv(self.tasks, self.name)

    def remove(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            save_TDL_as_csv(self.tasks, self.name)


list_of_TDL = []
list_of_task = []


while True:
    print("\n=== MAIN MENU ===")
    print("exit: 0")
    print("task section: 1")
    print("ToDoList section: 2")

    command = input("enter number: ")

    if command == "0":
        break

    elif command == "1":
        while True:
            print("\n--- TASK SECTION ---")
            print("back: 0")
            print("create task: 1")
            print("show tasks: 2")

            command = input("enter number: ")

            if command == "0":
                break

            elif command == "1":
                new_task = create_task()
                list_of_task.append(new_task)
                print("task created!")

            elif command == "2":
                if not list_of_task:
                    print("no tasks yet")
                else:
                    for i, task in enumerate(list_of_task):
                        print(f"{i}. {task}")

            else:
                print("invalid input")

    elif command == "2":
        while True:
            print("\n--- TODOLIST SECTION ---")
            print("back: 0")
            print("create ToDoList: 1")
            print("open ToDoList: 2")
            print("show ToDoLists: 3")

            command = input("enter number: ")

            if command == "0":
                break

            elif command == "1":
                name = input("enter ToDoList name: ")
                new_TDL = TDL(name)
                list_of_TDL.append(new_TDL)
                print("ToDoList created!")

            elif command == "2":
                name = input("enter ToDoList name: ")

                selected = None
                for tdl in list_of_TDL:
                    if tdl.name == name:
                        selected = tdl

                if not selected:
                    print("ToDoList not found")
                    continue

                while True:
                    print(f"\n--- {selected.name} ---")
                    print("back: 0")
                    print("show tasks: 1")
                    print("add task: 2")
                    print("remove task: 3")

                    command = input("enter number: ")

                    if command == "0":
                        break

                    elif command == "1":
                        selected.info()

                    elif command == "2":
                        if not list_of_task:
                            print("no tasks to add")
                            continue

                        for i, task in enumerate(list_of_task):
                            print(f"{i}. {task.title} (imp:{task.imp})")

                        choice = int(input("choose task number: "))
                        selected.add(list_of_task[choice])
                        print("task added!")

                    elif command == "3":
                        if not selected.tasks:
                            print("no tasks to remove")
                            continue

                        for i, task in enumerate(selected.tasks):
                            print(f"{i}. {task.title}")

                        choice = int(input("choose number: "))
                        selected.remove(selected.tasks[choice])
                        print("task removed!")

                    else:
                        print("invalid input")

            elif command == "3":
                for tdl in list_of_TDL:
                    print(tdl)

            else:
                print("invalid input")

    else:
        print("invalid command")
