from finding.Finding import Finding, FindingType, FindingStatus, FindingClassification, Confidentiality,\
    ImpactLevel, Integrity, Availability, Posture, Relevance, EffectivenessRating, SeverityCategoryCode
from database.db import Db
from analyst.analyst import Analyst

class FindingHandler:
    def __init__(self, finding: list = []):
        self.__finding = finding
        self.__database = Db.getInstance()


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

        new_finding.setid(self.__updateFinding(analyst= analyst, finding= new_finding))
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
        self.__finding = self.__getAllFindings()

    def __updateDatabase(self, finding: Finding, analyst: Analyst):
        id = self.__updateFinding(finding=finding, analyst= analyst)
        return id


    def __updateFinding(self, analyst, finding):
        findingDoc = finding.toDocument()
        analystDoc = analyst.toDocument()
        item_id = self.__database.storeFinding(findingDoc, analystDoc)
        return item_id

    def __deleteFinding(self, analyst, finding):
        findingDoc = finding.toDocument()
        analystDoc = analyst.toDocument()
        self.__database.removeFinding(findingDoc, analystDoc)
        return

    def __getFinding(self, finding):
        findingDoc = finding.toDocument()
        return Finding.convertDocument(self.__database.findFinding(findingDoc))


    def __getAllFindings(self):
        findingDocList = self.__database.getAllFindings()
        findingList = []
        for document in findingDocList:
            findingList.append(Finding.convertDocument(document))
        return findingList


