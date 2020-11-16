from PIL import Image
class Attachment:
    def __init__(self, attachment, file_name: str = "", _id= -1):
        self.__attachment = attachment
        self.__file_name = file_name
        self.__id = _id

    def viewFile(self):
        Image.open(self.__attachment).show()

    def getFileName(self):
        return self.__file_name

    def getAttachment(self):
        return self.__attachment

    def getId(self):
        return self.__id

