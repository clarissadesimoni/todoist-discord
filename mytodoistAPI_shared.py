#!/usr/bin/env python

from datetime import date, datetime, timedelta
import todoist
import pyperclip

token = 'INSERT TODOIST TOKEN HERE'
dir = 'INSERT DIRECTORY WHERE THE TXT FILE IS STORED' #ADD THE FINAL SLASH

def bullet(t):
    emotes = {      #this dictionary transforms the priority number into a colored emoji, so that you can visualize them quicker (emojis from FSC Discord server)
        1: ':mdot_red',
        2: ':mdot_orange',
        3: ':mdot_yellow',
        4: ':mdot_lavender'
    }
    ls = getLabel('Started')
    if t['in_history'] == 1 or (
            try_parsing_datetime(t['due']['date']).date() > date.today() and t['due']['is_recurring'] is True):
        return ':mdot_greencomp: '      #if the task is completed, the emoji will be green
    elif t['due']['is_recurring'] is True:
        if ls in t['labels']:
            return ':mdot_bluestart: '      #if the task is recurring, the emoji will be blue
        else:
            return ':mdot_blue: '
    elif ls in t['labels']:
        return emotes[5 - t['priority']] + 'start: '      #this snippet parses the priority so that it can select the right emoji
    elif t['due']['is_recurring'] is False and try_parsing_datetime(t['due']['date']).date() > date.today():
        return emotes[5 - t['priority']] + 'mig: '
    else:
        return emotes[5 - t['priority']] + ': '


def toString(t):        #this puts together the name of the task with its emoji
    return '\n' + bullet(t) + t['content']


def getLabel(name):     #helper function to get the ID of a label (for sorting reasons later on)
    api = todoist.TodoistAPI(token)
    api.sync()
    for label in api.state['labels']:
        if label['name'] == name:
            return label['id']


def try_parsing_datetime(text):     #helper function to get the date and time of a task as a datetime object
    if text is None:
        return date.today() + timedelta(days=1)
    if text == datetime.strftime(datetime.now(), "%Y-%m-%d"):
        text += "T00:00:00"     #if a time is not specified, midnight will be used
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return datetime.today() + timedelta(days=1)


def getTodoist():       #this functions gets all the tasks from todoist and filters the one due in the current date. Returns the list of IDs of the tasks
    data = []
    api = todoist.TodoistAPI(token)
    api.sync()
    ld = getLabel('Discord')        #this adds more filtering: since I do not want to show all my tasks, I add this label to the ones I want to show. If the name of the label you want to use is different, change also the parameter of this function
    for item in api.state['items']:
        if item['checked'] == 0 and item['due'] is not None and ld in item['labels']:
            if try_parsing_datetime(item['due']['date']).date() <= date.today():
                data.append(item['id'])
    return data


def getFile():      #function to get all the task IDs stored in the txt files
    f = open(dir + date.today().strftime('%Y%m%d') + '.txt', 'r+')
    data = []
    lines = f.readlines()
    f.close()
    if len(lines) > 0:
        for line in lines:
            data.append(int(line))
    return data


def compareLists(oldlist, newlist):      #helper function to add new tasks to the list of IDs (if there are any)
    if len(oldlist) == 0:
        return newlist
    else:
        data = []
        for n in newlist:
            data.append(n)
        for o in oldlist:
            if o not in newlist:
                data.append(o)
        return data


def updateFile(tasks):      #function to update the txt file with new tasks (if there are any)
    f = open(dir + date.today().strftime('%Y%m%d') + '.txt', 'w')
    for t in tasks:
        f.write(str(t) + '\n')


def flipBoolToInt(toFlip):      #helper function to transform bool to int for sorting purposes
    if toFlip is True:
        return 1
    else:
        return 0


def createString(tocopy):       #this function puts together all the tasks. It retrieves the data of the tasks using IDs, sorts the tasks and recursively adds the taks name with its bullet to the final string
    string = "Today's tasklist: (update at " + datetime.now().strftime('%I:%M %p') + ")"
    api = todoist.TodoistAPI(token)
    api.sync()
    tasks = []
    for i in tocopy:
        tasks.append(api.items.get(i)['item'])
    tasks.sort(key=lambda el: (flipBoolToInt(el['due']['is_recurring']), -el['priority'], el['due']['date']))
    firstRec = 0
    for t in tasks:
        if t['due']['is_recurring'] is True:
            firstRec = tasks.index(t)
            break
    tasks[firstRec:].sort(key=lambda el: el['content'])
    for x in tasks:
        string += toString(x)
    return string


def main():
    newVal = getTodoist()
    oldVal = getFile()
    toUse = compareLists(oldVal, newVal)
    updateFile(toUse)
    pyperclip.copy(createString(toUse))     #this copies the final string to the clipboard so that it's ready to paste it


main()
