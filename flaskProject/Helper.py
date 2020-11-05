import socket

# Helper class
from app import db


def cleanDB(subtasks,tasks,systems,events, analysts,analyst):
    # delete current event, systems, everything from the db, to handle only one event at a time
    for subtask in subtasks:
        db.deleteSubtask(analyst, subtask)
    for task in tasks:
        db.deleteTask(analyst, task)
    for system in systems:
        db.deleteSystem(analyst, system)
    for analyst in analysts:
        db.deleteAnalyst(analyst)
    for event in events:
        db.deleteEvent(analyst, event)


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True
