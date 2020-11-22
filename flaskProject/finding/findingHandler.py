from flaskProject.finding.Finding import Finding, FindingType, FindingStatus, FindingClassification, Confidentiality,\
    ImpactLevel, Integrity, Availability, Posture, Relevance, EffectivenessRating, SeverityCategoryCode
from flaskProject.database.databaseHandler import DatabaseHandler
from flaskProject.analyst.analyst import Analyst


class FindingHandler:
    def __init__(self, finding: list = []):
        self.__finding = finding
        self.__database = DatabaseHandler()


    #return a finding that was being searched for
    def getFinding(self, findingId):
        for item in self.__finding:
            if item.getid() == findingId:
                return item

    #return all findings
    def getAllFindings(self):
        return self.__finding

    #add a finding to the end of the list
    def appendFinding(self,
                      analyst,
                      hostName: str,
                      ipPort: str,
                      description: str,
                      status: FindingStatus,
                      type: FindingType,
                      classification: FindingClassification,
                      associationToFinding: list,
                      evidence,
                      archiveStatus: bool,
                      confidentiality: Confidentiality,
                      integrity: Integrity,
                      availability: Availability,
                      analystAssigned: list,
                      posture: Posture,
                      mitigationBriefDescription: str,
                      mitigationLongDescription: str,
                      relevance: Relevance,
                      countermeasureEffectivenessRating: EffectivenessRating,
                      impactDescription: str,
                      impactLevel: ImpactLevel,
                      severityCategoryCode: SeverityCategoryCode,
                      longDescription: str = "",
                      collaboratorAssigned: list = [],
                      associatedTask=-1,
                      id=-1
                      ):

        new_finding = Finding(hostName= hostName,
                              ipPort= ipPort,
                              description= description,
                              status= status,
                              type= type,
                              classification= classification,
                              associationToFinding= associationToFinding,
                              evidence= evidence,
                              archiveStatus= archiveStatus,
                              confidentiality= confidentiality,
                              integrity= integrity,
                              availability= availability,
                              analystAssigned= analystAssigned,
                              posture= posture,
                              mitigationBriefDescription= mitigationBriefDescription,
                              mitigationLongDescription= mitigationLongDescription,
                              relevance= relevance,
                              countermeasureEffectivenessRating= countermeasureEffectivenessRating,
                              impactDescription=impactDescription,
                              impactLevel= impactLevel,
                              severityCategoryCode= severityCategoryCode,
                              longDescription = longDescription,
                              collaboratorAssigned= collaboratorAssigned,
                              associatedTask=associatedTask,
                              id= id)

        new_finding.setid(self.__database.updateFinding(analyst= analyst, finding= new_finding))
        self.__finding.append(new_finding)
        return

    #update a specified finding that is in the list
    def updateFinding(self, finding: Finding, analyst: Analyst):

        index = 0
        while index < len(self.__finding):
            if self.__finding[index].getid() == finding.getid():
                self.__finding[index] = finding
                self.__updateDatabase(finding= finding, analyst=analyst)
                return
            index += 1


    def loadFindings(self):
        self.__finding = self.__database.getAllFindings()

    def __updateDatabase(self, finding: Finding, analyst: Analyst):
        id = self.__database.updateFinding(finding=finding, analyst= analyst)
        return id
