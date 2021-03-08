import os
import random

from github import Github
from tabulate import tabulate

g = Github(os.environ.get("GITHUB_TOKEN"))
repo = g.get_user().get_repo("technicie-biero-test")
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
    "Drinking issue",
    "Apply new drinking guidelines",
    "Introduce Beer API v2",
    "beer.exe has crashed on AlcoholException",
    "Loading CraftBeerModule failed, try again",
    "Add new shot app",
    "Add Gall&Gall sync",
    "Kernel panic, switching to shots",
    "Add @Alcoholic annotations",
    "Enrich AlcoholPreprocessors",
    "Poor pils in CI pipeline",
    "DrinkingBufferOverflow crashes on 500",
    "Fix Segfault in beer tap",
    "Implement AlcoholCongestionControl",
    "Prevent Sentry from reporting laffe borrelaars",
    "Rewrite app to Flugel",
    "Fix HTTP 428 I'm a beer crate",
    "Solve HTTP 413 alcohol payload too large",
    "Member statistics is missing drinking data",
    "Add alcohol percentage to statistics page",
    "Unexpected HTTP 404 drink not found",
    "Refactor soda with beer in drinking app",
    "Improve alcohol coverage",
    "Investigate pycraftbeer library",
    "Increase alcohol coverage percentage",
    "Initial Adt",
    "Remove DRIVINGLICENSE due to alcohol misbehavior",
    "Add ContentShotPolicy to nginx config",
    "Update ADTME.md",
    "Undo alcohol minimization",
    "ValidationError while parsing new drinks",
    "Allow beer consumption in future",
    "Add BeerDocker to crafttab",
    "Create beer command to bierobot",
    "Change primary color to gold-fellow-yellow",
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
    number = int(input("How many? (there are 15 participants) "))
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
        name = input("Give custom name (leave empty for random generation): ")
        if name == "":
            name = None
        create_issue(kind, name=name, assignee=person)
        print(f"Created a {kind.name}{' for '+ str(person.name) if person else ''}🍺")
    else:
        for _ in range(number):
            create_issue(kind, assignee=person)
        print(
            f"Created {number} {kind.name}s{' for '+ str(person.name) if person else ''}🍺"
        )


def emergency_adt():
    name = input("Give custom name (leave empty for automatic generation): ")
    if name == "":
        name = "CRITICAL BUG HOTFIX 🍻⏱"
    for person in users:
        if person in admins:
            break
        _, card = create_issue(
            get_type("adt"), name=name, assignee=user(person), col=drinking
        )
    print("🍻⏱ Emergency adt launched for every person.")

def stats():
    print("Displaying the statistics for every person")
    output = []
    headers = ["Name", f"total ({repo.get_issues(state='all').totalCount})", f"open ({repo.get_issues(state='open').totalCount})", f"closed ({repo.get_issues(state='closed').totalCount})"]
    for person in users:
        if person in admins:
            break
        u = user(person)
        total = repo.get_issues(assignee=u)
        open = repo.get_issues(state="open", assignee=u)
        closed = repo.get_issues(state="closed", assignee=u)
        output.append([person, total.totalCount, open.totalCount, closed.totalCount])

    total = repo.get_issues(assignee="none")
    open = repo.get_issues(state="open", assignee="none")
    closed = repo.get_issues(state="closed", assignee="none")
    output.append(["unassigned", total.totalCount, open.totalCount, closed.totalCount])

    print(tabulate(output, headers=headers))


commands = {
    "Create a new issue 🍺/🥃/🍹": create,
    "Launch an emergency adt 🍻⏱": emergency_adt,
    "Show statistics on many everyone drank ⁉️": stats,
}


def main():
    while True:
        print("The following actions are available")
        for i, x in enumerate(commands):
            print(f"[{i+1}] {x}")
        task = int(input("What do you want to do? "))
        commands[list(commands.keys())[task - 1]]()
        print("")


if __name__ == "__main__":
    main()
