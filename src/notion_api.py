#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

from datetime import datetime

from notion.client import NotionClient
from notion.block import DividerBlock, TextBlock

from config import notionToken, tagsDatabaseURL, tasksDatabaseURL, winsDatabaseURL, yearPageURL


def client():
    return NotionClient(token_v2=notionToken())


def tagsDatabase():
    return client().get_collection_view(tagsDatabaseURL())


def tasksDatabase():
    return client().get_collection_view(tasksDatabaseURL())


def winsDatabase():
    return client().get_collection_view(winsDatabaseURL())


def currentDayTasksDatabase():
    return currentDay().children[2]


def currentYear():
    return client().get_block(yearPageURL())


def currentWeek():
    currentWeek = None
    currentDate = datetime.now()

    # Sunday Starts the week
    weekNumber = str(currentDate.isocalendar()[
                     1] + (currentDate.isoweekday() == 7))

    for weekPage in currentYear().children:
        if weekPage.title.startswith("Week " + weekNumber):
            currentWeek = weekPage
            break
        else:
            next

    return currentWeek


def currentDay():
    currentDay = None
    currentDate = datetime.now()

    dayNumber = str(currentDate.day)
    monthName = currentDate.strftime("%B")
    daysPage = currentWeek().children[1].children[1]

    for dayPage in daysPage.children:
        if dayPage.title.startswith(monthName + " " + dayNumber):
            currentDay = dayPage
            break
        else:
            next

    return currentDay


def appendToCurrentDayNotes(content):
    # Get the divider block that signifies the end of the notes for the current day
    dividerBlock = [x for x in currentDay().children if type(x)
                    == DividerBlock][0]

    # Add note to end of the page, then move it to before the divider
    noteBlock = currentDay().children.add_new(TextBlock, title=content)
    noteBlock.move_to(dividerBlock, "before")

    return noteBlock
