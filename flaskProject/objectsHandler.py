# from analyst.analyst import Analyst
# from event.event import Event
# from finding.Finding import Finding
# from system.system import System
# from task.subtask import Subtask
# from task.task import Task
#
#
# def createAnalyst(fname, lname, initials, title, role):
#     analyst = Analyst(fname, lname,
#                       initials, title,
#                       role)
#     return analyst
#
#
# def createEvent(name, description, type, version, assessmentDate, SCTG, organizationName, classification, classifiedBy,
#                 DerivedFrom, declassificcationDate, customerName, archived, analystlist):
#     event = Event(name,
#                   description,
#                   type,
#                   version,
#                   assessmentDate,
#                   SCTG,
#                   organizationName,
#                   classification,
#                   classifiedBy,
#                   DerivedFrom,
#                   declassificcationDate,
#                   customerName,
#                   archived,
#                   analystlist)
#     return event
#
#
# def createSystem(name, description,locations,routers,switches, rooms,testplan,archived,confidentiality,integrity,avaailability):
#     system = System(name,
#                     description,
#                     locations,
#                     routers,
#                     switches,
#                     rooms,
#                     testplan,
#                     archived,
#                     confidentiality,
#                     integrity,
#                     avaailability)
#     return system
#
#
# def createTask(name,description,priority,progress,dueDate,attachment,associationToTask,analyst,collaborator, archived):
#     task = Task(name,
#                 description,
#                 priority,
#                 progress,
#                 dueDate,
#                 attachment,
#                 associationToTask,
#                 analyst,
#                 collaborator,
#                 archived)
#     return task
#
#
# def createSubtask(name, description, progress,dueDate, attachment,association,analyst,collaborator,archived):
#     subtask = Subtask(name,
#                       description,
#                       progress,
#                       dueDate,
#                       attachment,
#                       association,
#                       analyst,
#                       collaborator, archived)
#     return subtask
#
#
# def createFinding(hostName, ipPort, description, status, type,classification,association,evidence, archived,
#                   confidentiality,integrity,availability,analyst,posture,mitigationDescription,mitigationLongDescription,
#                   relevance,effectiveness,impactDescriptioin,impactLevel,SeverityCategoryCode,longDescription,collaborators):
#     finding = Finding(hostName,
#                       ipPort,
#                       description,
#                       status,
#                       type,
#                       classification,
#                       association,
#                       evidence,
#                       archived,
#                       confidentiality,
#                       integrity,
#                       availability,
#                       analyst,
#                       posture,
#                       mitigationDescription,
#                       mitigationLongDescription,
#                       relevance,
#                       effectiveness,
#                       impactDescriptioin,
#                       impactLevel,
#                       SeverityCategoryCode,
#                       longDescription,
#                       collaborators)
#     return finding