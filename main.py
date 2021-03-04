import os
import random

from github import Github

g = Github(os.environ.get("GITHUB_TOKEN"))
repo = g.get_user().get_repo("technicie-biero")
board = repo.get_projects()[0]

columns = board.get_columns()
to_drink = columns[0]
drinking = columns[1]
done = columns[2]

users = {
    # "jelle": "pingiun",
    # "sebas": "se-bastiaan",
    # "wouter": "wdoeland",
    # "jen": "jendusseljee",
    # "quinten": "ColonelPhantom",
    # "simcha": "9Y0",
    # "pepijn": "PepijnRezelman",
    # "luca": "Luca-Castelnuovo",
    # "mark": "mark-boute",
    # "ted": "Tedddooo",
    # "johannes": "PeaceDucko",
    # "dirk": "DeD1rk",
    # "jorrit": "Jorritdeboer",
    # "mario": "mtsatsev",
    # "luc": "LCKnol",
    "lars": "KiOui",
    "job": "jobdoesburg",
}

admins = [
    # "lars", "job"
]


def user(name):
    return g.get_user(users[name])


def ask_user():
    person = input("Who? ")
    if person not in users:
        print("I don't know that name...")
        return ask_user()
    return user(person)


types = {"craft": "craft beer", "beer": "beer", "shot": "shot", "adt": "adt"}

titles = [
    "De keel moet gesmeerd worden",
    "HertogJanFactory needs more consumers",
    "throat.py needs more pils",
]


def get_random_title():
    return random.choice(titles)


def get_type(name):
    return repo.get_label(types[name])


def ask_type():
    inp = input("Type? ")
    if inp not in types:
        print("I don't know that type...")
        return ask_type()
    return get_type(inp)


def ask_how_many():
    number = int(input("How many? "))
    if not number > 1:
        print("I don't know what to do...")
        return ask_how_many()
    return number


def create_issue(label, name=None, assignee=None, col=to_drink):
    if name is None:
        name = get_random_title()
    issue = repo.create_issue(name)
    issue.add_to_labels(label)
    if assignee:
        issue.add_to_assignees(assignee)
    card = col.create_card(content_id=issue.id, content_type="Issue")
    return issue, card


def create():
    person = None
    resp = input("Pre-assigned? (y/N) ")
    if resp == "y":
        person = ask_user()

    kind = ask_type()

    number = int(input("How many? "))

    if number == 1:
        create_issue(kind, person)
        print(f"Created a {kind.name}{' for '+ str(person.name) if person else ''}🍺")
    else:
        for _ in range(number):
            create_issue(kind, person)
        print(
            f"Created {number} {kind.name}s{' for '+ str(person.name) if person else ''}🍺"
        )


def emergency_adt():
    for person in users:
        if person in admins:
            break
        _, card = create_issue(
            get_type("adt"), "CRITICAL BUG - HOTFIX 🍻⏱", user(person), col=drinking
        )
    print("🍻⏱ Emergency adt launched for every person.")


commands = {
    "Create a new issue 🍺/🥃/🍹": create,
    "Launch an emergency adt 🍻⏱": emergency_adt,
}


def main():
    while True:
        print("The following actions are available")
        for i, x in enumerate(commands):
            print(f"[{i+1}] {x}")
        task = int(input("What do you want to do? "))
        commands[list(commands.keys())[task - 1]]()
        print("\n")


if __name__ == "__main__":
    main()
