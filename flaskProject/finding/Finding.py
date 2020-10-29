from finding.findingStatus import FindingStatus
from finding.findingType import FindingType
from finding.findingClassification import FindingClassification
from security_objectives.integrity import Integrity
from security_objectives.confidentiality import Confidentiality
from security_objectives.availability import Availability
from finding.posture import Posture
from finding.relevance import Relevance
from finding.effectivenessRating import EffectivenessRating
from finding.impactLevel import ImpactLevel
from finding.severityCategoryCode import SeverityCategoryCode


class Finding:
    def __init__(self,
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
                 id = -1):

        self.__id = id
        self.__hostName = hostName
        self.__ipPort = ipPort
        self.__description = description
        self.__longDescription = longDescription
        self.__status = status
        self.__type = type
        self.__classification = classification
        self.__associationToFinding = associationToFinding
        self.__evidence = evidence
        self.__archiveStatus = archiveStatus
        self.__confidentiality = confidentiality
        self.__integrity = integrity
        self.__availability = availability
        self.__analystAssigned = analystAssigned
        self.__collaboratorAssigned = collaboratorAssigned
        self.__posture = posture
        self.__mitigationBriefDescription = mitigationBriefDescription
        self.__mitigationLongDescription = mitigationLongDescription
        self.__threatRelevance = relevance
        self.__countermeasureEffectivenessRating = countermeasureEffectivenessRating
        self.__impactDescription = impactDescription
        self.__impactLevel = impactLevel
        self.__severityCategoryCode = severityCategoryCode
        self.__severityCategoryScore = self.__severityCategoryCode.value
        self.__confidentialityFindingImpactOnSystem = self.__confidentiality
        self.__integrityFindingImpactOnSystem = self.__integrity
        self.__availabilityFindingImpactOnSystem = self.__availability
        self.__impactScore = self.__deriveImpactScore(self.__confidentialityFindingImpactOnSystem
                                                       , self.__integrityFindingImpactOnSystem
                                                       , self.__availabilityFindingImpactOnSystem)
        self.__vulnerabilitySeverity = self.__deriveVunarabilitySeverity()
        self.__qualitativeVulnerabilitySeverity:str  = self.__deriveQualitaiveVulnerabilitySeverity()
        self.__likelihood = self.__deriveLikelihood()
        self.__assessedRisk = self.__deriveRisk()




    #Setters
    def setid(self, id):
        self.__id = id

    def setHostName(self, hostName: str):
        self.__hostName = hostName

    def setIpPort(self, ipPort: str):
        self.__ipPort = ipPort

    def setDescription(self, description):
        self.__description = description

    def setLongDescription(self, longDescription: str):
        self.__longDescription = longDescription

    def setStatus(self, status: FindingStatus):
        self.__status = status

    def setType(self, type: FindingType):
        self.__type = type

    def setClassification(self, classification: FindingClassification):
        self.__classification = classification

    def setAssociationTo(self, associationTo: list):
        self.__associationTo = associationTo

    def setEvidence(self, evidence):
        self.__evidence = evidence

    def setArchiveStatus(self, archiveStatus: bool):
        self.__archiveStatus = archiveStatus

    def setConfidentiality(self, confidentiality: Confidentiality):
        self.__confidentiality = confidentiality

    def setIntegrity(self,integrity: Integrity):
        self.__integrity = integrity

    def setAvailability(self, availability: Availability):
        self.__availability = availability

    def setAnalystAssigned(self, analystAssigned: list):
        self.__analystAssigned = analystAssigned

    def setCollaboratorAssigned(self, collaboratorAssigned: list):
        self.__collaboratorAssigned = collaboratorAssigned

    def setPosture(self, posture: Posture):
        self.__posture = posture

    def setMitigationBriefDescription(self, mitigationBriefDescription: str):
        self.__mitigationBriefDescription = mitigationBriefDescription

    def setMitigationLongDescription(self, mitigationLongDescription: str):
        self.__mitigationLongDescription = mitigationLongDescription

    def setRelevance(self, relevance: Relevance):
        self.__threatRelevance = relevance
        self.__likelihood == self.__deriveLikelihood()
        self.__assessedRisk = self.__deriveRisk()

    def setCountermeasureEffectivenessRating(self, countermeasureEffectivenessRating: EffectivenessRating):
        self.__countermeasureEffectivenessRating = countermeasureEffectivenessRating
        self.__vulnerabilitySeverity = self.__deriveVunarabilitySeverity()
        self.__qualitativeVulnerabilitySeverity = self.__deriveQualitaiveVulnerabilitySeverity()
        self.__likelihood = self.__deriveLikelihood()
        self.__assessedRisk = self.__deriveRisk()


    def setImpactDescription(self, impactDescription: str):
        self.__impactDescription = impactDescription

    def setImpactLevel(self, impactLevel: ImpactLevel):
        self.__impactLevel = impactLevel
        self.__assessedRisk = self.__deriveRisk()

    def setSeverityCategoryCode(self, severityCategoryCode: SeverityCategoryCode):
        self.__severityCategoryCode = severityCategoryCode
        self.__severityCategoryScore = self.__severityCategoryCode.value
        self.__vulnerabilitySeverity = self.__deriveVunarabilitySeverity()
        self.__qualitativeVulnerabilitySeverity = self.__deriveQualitaiveVulnerabilitySeverity()
        self.__likelihood = self.__deriveLikelihood()
        self.__assessedRisk = self.__deriveRisk()

    def setImpactScore(self):
        self.__impactScore = self.__deriveImpactScore(self.__confidentiality, self.__integrity, self.__availability)


    #Getters
    def getid(self):
        return self.__id

    def getHostName(self):
        return self.__hostName

    def getIpPort(self):
        return self.__ipPort

    def getDescription(self):
        return self.__description

    def getLongDescription(self):
        return self.__longDescription

    def getStatus(self):
        return self.__status

    def getType(self):
        return self.__type

    def getClassification(self):
         return self.__classification

    def getAssociationTo(self):
        return self.__associationToFinding

    def getEvidence(self):
        return self.__evidence

    def getArchiveStatus(self):
        return self.__archiveStatus

    def getConfidentiality(self):
        return self.__confidentiality

    def getIntegrity(self):
        return self.__integrity

    def getAvailability(self):
        return self.__availability

    def getAnalystAssigned(self):
        return self.__analystAssigned

    def getCollaboratorsAssigned(self):
        return self.__collaboratorAssigned

    def getPosture(self):
        return self.__posture

    def getMitigationBriefDescription(self):
        return self.__mitigationBriefDescription

    def getMitigationLongDescription(self):
        return self.__mitigationLongDescription

    def getRelevance(self):
        return self.__threatRelevance

    def getCountermeasureEffectivenessRating(self):
        return self.__countermeasureEffectivenessRating

    def getImpactDescription(self):
        return self.__impactDescription

    def getImpactLevel(self):
        return self.__impactLevel

    def getSeverityCategoryCode(self):
        return self.__severityCategoryCode

    def getSeverityCategoryScore(self):
        return self.__severityCategoryScore

    def getVulnerabilitySeverity(self):
        return self.__vulnerabilitySeverity

    def getQualitativeVulnerabilitySeverity(self):
        return self.__qualitativeVulnerabilitySeverity

    def getRisk(self):
        return self.__assessedRisk

    def getLikelihood(self):
        return self.__likelihood

    def getConfidentialityFindingImpactOnSystem(self):
        return self.__confidentialityFindingImpactOnSystem

    def getIntegrityFindingImpactOnSystem(self):
        return self.__integrityFindingImpactOnSystem

    def getAvailabilityFindingImpactOnSystem(self):
        return self.__availabilityFindingImpactOnSystem

    def getImpactScore(self):
        return self.__impactScore

    def toDocument(self):
        if self.__id == -1:
            findingDoc = {
                "hostname": self.__hostName,
                "ipPort": self.__ipPort,
                "description": self.__description,
                "longDescription": self.__longDescription,
                "status": self.__status,
                "type": self.__type,
                "classification": self.__classification,
                "associatedTo": self.__associationToFinding,
                "evidence": self.__evidence,
                "archiveStatus": self.__archiveStatus,
                "confidentiality": self.__confidentiality,
                "integrity": self.__integrity,
                "availability": self.__availability,
                "analystAssigned": self.__analystAssigned,
                "collaboratorAssigned": self.__collaboratorAssigned,
                "posture": self.__posture,
                "mitigationBriefDescription": self.__mitigationBriefDescription,
                "mitigationLongDescription": self.__mitigationLongDescription,
                "threatRelevance": self.__threatRelevance,
                "countermeasureEffectivenessRating": self.__countermeasureEffectivenessRating,
                "impactDescription": self.__impactDescription,
                "impactLevel": self.__impactLevel,
                "severityCategoryCode": self.__severityCategoryCode,
                "severityCategoryScore": self.__severityCategoryScore,
                "confidentialityFindingImpactOnSystem": self.__confidentialityFindingImpactOnSystem,
                "integrityFindingImpactOnSystem": self.__integrityFindingImpactOnSystem,
                "availabilityFindingImpactOnSystem": self.__availabilityFindingImpactOnSystem,
                "impactScore": self.__impactScore,
                "vulnerabilitySeverity": self.__vulnerabilitySeverity,
                "qualitativeVulnerabilitySeverity": self.__qualitativeVulnerabilitySeverity,
                "likelihood": self.__likelihood,
                "assessedRisk": self.__assessedRisk



            }
            return findingDoc
        else:
            findingDoc = {
                "_id": self.__id,
                "hostname": self.__hostName,
                "ipPort": self.__ipPort,
                "description": self.__description,
                "longDescription": self.__longDescription,
                "status": self.__status,
                "type": self.__type,
                "classification": self.__classification,
                "associatedTo": self.__associationTo,
                "evidence": self.__evidence,
                "archiveStatus": self.__archiveStatus,
                "confidentiality": self.__confidentiality,
                "integrity": self.__integrity,
                "availability": self.__availability,
                "analystAssigned": self.__analystAssigned,
                "collaboratorAssigned": self.__collaboratorAssigned,
                "posture": self.__posture,
                "mitigationBriefDescription": self.__mitigationBriefDescription,
                "mitigationLongDescription": self.__mitigationLongDescription,
                "threatRelevance": self.__threatRelevance,
                "countermeasureEffectivenessRating": self.__countermeasureEffectivenessRating,
                "impactDescription": self.__impactDescription,
                "impactLevel": self.__impactLevel,
                "severityCategoryCode": self.__severityCategoryCode,
                "severityCategoryScore": self.__severityCategoryScore,
                "confidentialityFindingImpactOnSystem": self.__confidentialityFindingImpactOnSystem,
                "integrityFindingImpactOnSystem": self.__integrityFindingImpactOnSystem,
                "availabilityFindingImpactOnSystem": self.__availabilityFindingImpactOnSystem,
                "impactScore": self.__impactScore,
                "vulnerabilitySeverity": self.__vulnerabilitySeverity,
                "qualitativeVulnerabilitySeverity": self.__qualitativeVulnerabilitySeverity,
                "likelihood": self.__likelihood,
                "assessedRisk": self.__assessedRisk
            }
            return findingDoc

    @staticmethod
    def convertDocument(document):
        return Finding(document["hostname"],
                       document["ipPort"],
                       document["description"],
                       FindingStatus.getMember(document["status"]),
                       FindingType.getMember(document["type"]),
                       FindingClassification.getMember(document["classification"]),
                       document["associatedTo"],
                       document["evidence"],
                       document["archiveStatus"],
                       Confidentiality.getMember(document["confidentiality"]),
                       Integrity.getMember(document["integrity"]),
                       Availability.getMember(document["availability"]),
                       document["analystAssigned"],
                       Posture.getMember(document["posture"]),
                       document["mitigationBriefDescription"],
                       document["mitigationLongDescription"],
                       Relevance.getMember(document["threatRelevance"]),
                       EffectivenessRating.getMember(document["countermeasureEffectivenessRating"]),
                       document["impactDescription"],
                       ImpactLevel.getMember(document["impactLevel"]),
                       SeverityCategoryCode.getMember(document["severityCategoryCode"]),
                       document["longDescription"],
                       document["collaboratorAssigned"],
                       document["_id"])

    # derive likelihood methods are helper methods for __deriveLikelihood
    # these should be changed to derive the value in a programmatic way if time allows for it
    def __derivePossibleLikelihood(self):
        if self.__qualitativeVulnerabilitySeverity == "Very Low":
            return "VL"
        elif self.__qualitativeVulnerabilitySeverity == "Low":
            return "VL"
        elif self.__qualitativeVulnerabilitySeverity == "Medium":
            return "L"
        elif self.__qualitativeVulnerabilitySeverity == "High":
            return "L"
        elif self.__qualitativeVulnerabilitySeverity == "Very High":
            return "L"

    def __derivePredictedLikelihood(self):
        if self.__qualitativeVulnerabilitySeverity == "Very Low":
            return "VL"
        elif self.__qualitativeVulnerabilitySeverity == "Low":
            return "L"
        elif self.__qualitativeVulnerabilitySeverity == "Medium":
            return "L"
        elif self.__qualitativeVulnerabilitySeverity == "High":
            return "L"
        elif self.__qualitativeVulnerabilitySeverity == "Very High":
            return "M"

    def __deriveAnticipatedLikelihood(self):
        if self.__qualitativeVulnerabilitySeverity == "Very Low":
            return "VL"
        elif self.__qualitativeVulnerabilitySeverity == "Low":
            return "L"
        elif self.__qualitativeVulnerabilitySeverity == "Medium":
            return "M"
        elif self.__qualitativeVulnerabilitySeverity == "High":
            return "M"
        elif self.__qualitativeVulnerabilitySeverity == "Very High":
            return "H"

    def __deriveExpectedLikelihood(self):
        if self.__qualitativeVulnerabilitySeverity == "Very Low":
            return "VL"
        elif self.__qualitativeVulnerabilitySeverity == "Low":
            return "L"
        elif self.__qualitativeVulnerabilitySeverity == "Medium":
            return "M"
        elif self.__qualitativeVulnerabilitySeverity == "High":
            return "H"
        elif self.__qualitativeVulnerabilitySeverity == "Very High":
            return "VH"

    def __deriveConfirmedLikelihood(self):
        if self.__qualitativeVulnerabilitySeverity == "Very Low":
            return "VL"
        elif self.__qualitativeVulnerabilitySeverity == "Low":
            return "L"
        elif self.__qualitativeVulnerabilitySeverity == "Medium":
            return "M"
        elif self.__qualitativeVulnerabilitySeverity == "High":
            return "H"
        elif self.__qualitativeVulnerabilitySeverity == "Very High":
            return "VH"


    #derive impact level assessed risk are helper methods for __deriveRisk
    #these should be changed to derive the value in a programmatic way if time allows for it
    def __deriveInfoImpactLevelAssessedRisk(self):
        return "info"

    def __deriveVLImpactLevelAssessedRisk(self):
        return "VL"
    def __deriveLImpactLevelAssessedRisk(self):
        if self.__likelihood == "VL":
            return "VL"
        else:
            return "L"
    def __deriveMImpactLevelAssessedRisk(self):
        if (self.__likelihood == "VL") or (self.__likelihood == "L"):
            return "L"
        else:
            return "M"

    def __deriveHImpactLevelAssessedRisk(self):
        if (self.__likelihood == "VL") or (self.__likelihood == "L"):
            return "L"
        elif (self.__likelihood == "M"):
            return "M"
        else:
            return "H"

    def __deriveVHImpactLevelAssessedRisk(self):
        if self.__likelihood == "VL":
            return "L"
        elif self.__likelihood == "L":
            return "M"
        elif self.__likelihood == "M":
            return "H"
        else:
            return "VH"

    def __deriveVunarabilitySeverity(self):
        return ((self.__severityCategoryScore
                 * self.__impactScore
                 * self.__countermeasureEffectivenessRating.value)
                / 10)

    def __deriveRisk(self):
        if self.__impactScore == 0:
            return "info"

        else:
            if self.__impactLevel.value == 0:
                return self.__deriveInfoImpactLevelAssessedRisk()
            elif self.__impactLevel.value == 1:
                return self.__deriveVLImpactLevelAssessedRisk()
            elif self.__impactLevel.value == 2:
                return self.__deriveLImpactLevelAssessedRisk()
            elif self.__impactLevel.value == 3:
                return self.__deriveMImpactLevelAssessedRisk()
            elif self.__impactLevel.value == 4:
                return self.__deriveHImpactLevelAssessedRisk()
            elif self.__impactLevel.value == 5:
                return self.__deriveVHImpactLevelAssessedRisk()
            else:
                pass
            # deriveOptions = {
            #     0: self.__deriveInfoImpactLevelAssessedRisk,
            #     1: self.__deriveVLImpactLevelAssessedRisk,
            #     2: self.__deriveLImpactLevelAssessedRisk,
            #     3: self.__deriveMImpactLevelAssessedRisk,
            #     4: self.__deriveHImpactLevelAssessedRisk,
            #     5: self.__deriveVHImpactLevelAssessedRisk,
            # }
            # func = deriveOptions.get(self.__impactLevel.value, lambda: 'Invalid')
            # return func()

    def __deriveLikelihood(self):
        if self.__impactScore == 0:
            return "info"

        else:
            if self.__threatRelevance.value == 0:
                return self.__derivePossibleLikelihood()
            elif self.__threatRelevance.value == 1:
                return self.__derivePredictedLikelihood()
            elif self.__threatRelevance.value == 2:
                return self.__deriveAnticipatedLikelihood()
            elif self.__threatRelevance.value == 3:
                return self.__deriveExpectedLikelihood()
            elif self.__threatRelevance.value == 4:
                return self.__deriveConfirmedLikelihood()
            else:
                pass
            # deriveOptions = {
            #     0: self.__derivePossibleLikelihood,
            #     1: self.__derivePredictedLikelihood,
            #     2: self.__deriveAnticipatedLikelihood,
            #     3: self.__deriveExpectedLikelihood,
            #     4: self.__deriveConfirmedLikelihood
            # }
            # func = deriveOptions.get(self.__threatRelevance.value, lambda: 'Invalid')
            # return func()

    def __deriveQualitaiveVulnerabilitySeverity(self):
        if(self.__vulnerabilitySeverity >= 95 and self.__vulnerabilitySeverity <= 100):
            return "Very High"

        elif(self.__vulnerabilitySeverity >= 80 and self.__vulnerabilitySeverity < 95):
            return "High"

        elif(self.__vulnerabilitySeverity >= 20 and self.__vulnerabilitySeverity < 80):
            return "Medium"

        elif(self.__vulnerabilitySeverity >= 5 and self.__vulnerabilitySeverity < 20):
            return "Low"

        elif(self.__vulnerabilitySeverity >= 0 and self.__vulnerabilitySeverity < 5):
            return "Very Low"
        else:
            return ""

    def __deriveImpactScore(self, c: Confidentiality, i: Integrity, a: Availability):
        if (c == Confidentiality.HIGH) and (i == Integrity.HIGH) and (a == Availability.HIGH):
            return 10

        elif((c == Confidentiality.HIGH and i == Integrity.HIGH)
            or (c == Confidentiality.HIGH and a == Availability.HIGH)
            or (i == Integrity.HIGH and a == Availability.HIGH)):

            return 9

        elif(c == Confidentiality.HIGH
            or i == Integrity.HIGH
            or a == Availability.HIGH):

            return 8

        elif((c == Confidentiality.MEDIUM)
             and (i == Integrity.MEDIUM)
             and (a == Availability.MEDIUM)):
            return 7

        elif((c == Confidentiality.MEDIUM and i == Integrity.MEDIUM)
            or (c == Confidentiality.MEDIUM and a == Availability.MEDIUM)
            or (i == Integrity.MEDIUM and a == Availability.MEDIUM)):
            return 6

        elif((c == Confidentiality.MEDIUM
            or i == Integrity.MEDIUM
            or a == Availability.MEDIUM)):
            return 5

        elif((c == Confidentiality.LOW)
             and (i == Integrity.LOW)
             and (a == Availability.LOW)):
            return 4

        elif((c == Confidentiality.LOW and i == Integrity.LOW)
            or (c == Confidentiality.HIGH and a == Availability.LOW)
            or (i == Integrity.LOW and a == Availability.LOW)):
            return 3

        elif((c == Confidentiality.LOW
            or i == Integrity.LOW
            or a == Availability.LOW)):
            return 2

        else:
            return 0


