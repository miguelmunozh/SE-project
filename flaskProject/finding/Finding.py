from finding.findingStatus import FindingStatus
from finding.findingType import FindingType
from finding.findingClassification import FindingClassification

class Finding:
    def __init__(self,
                 hostName: str,
                 ipPort: str,
                 description: str,
                 longDescription: str,
                 status: FindingStatus,
                 type: FindingType,
                 classification: FindingClassification,
                 associationTo: list,
                 evidence,
                 archiveStatus: bool,
                 id = -1):

        self.__id = id
        self.__hostName = hostName
        self.__ipPort = ipPort
        self.__description = description
        self.__longDescription = longDescription
        self.__status = status
        self.__type = type
        self.__classification = classification
        self.__associationTo = associationTo
        self.__evidence = evidence
        self.__archiveStatus = archiveStatus


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

    def setArchioveStatus(self, archiveStatus: bool):
        self.__archiveStatus = archiveStatus


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
        return self.__associationTo

    def getEvidence(self):
        return self.__evidence

    def getArchioveStatus(self):
        return self.__archiveStatus


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
                "associatedTo": self.__associationTo,
                "evidence": self.__evidence,
                "archiveStatus": self.__archiveStatus
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
                "archiveStatus": self.__archiveStatus
            }
            return findingDoc

    @staticmethod
    def convertDocument(document):
        return Finding(document["hostname"],
                       document["ipPort"],
                       document["description"],
                       document["longDescription"],
                       FindingStatus.getMember(document["status"]),
                       FindingType.getMember(document["type"]),
                       FindingClassification.getMember(document["classification"]),
                       document["associatedTo"],
                       document["evidence"],
                       document["archiveStatus"],
                       document["_id"])


