from flaskProject.attachment.attachment import Attachment
from flaskProject.database.db import Db

class AttachmentHandler:
    def __init__(self, attachment_ids: list = []):
        self.__attachment: list = []
        self.__database = Db.getInstance()
        self.loadAttachments(attachment_ids)

    def find_attachment(self, id):
        for item in self.__attachment:
            if item.getId() == id:
                return item
        return None

    def find_and_open_attachment(self, id):
        for item in self.__attachment:
            if item.getId() == id:
                item.viewFile()

    # This algorithm attempts to create an instance of Attachment that has a type 'gridfs.grid_file.GridOut'
    # as the attachment argument. This type allows the attachment to be treated as a file,
    # while also giving access to additional meta data that was stored.

    def appendAttachment(self, path, attachment_name: str =""):
        id = self.__storeAttachment(path, file_name=attachment_name)
        file = self.__retrieveAttachment(id)
        self.__attachment.append(Attachment(attachment=file, file_name = attachment_name, _id= id))
        return id

    def loadAttachments(self, attachment_id: list):
        attachment_list = []
        for id in attachment_id:
            attachment_data = self.__retrieveAttachment(id)
            attachment_list.append(Attachment(attachment= attachment_data
                                                , file_name=attachment_data.filename
                                                , _id= attachment_data._id))
            self.__attachment = attachment_list

    def getAllAttachmentIds(self):
        idList = list
        for attachment in self.__attachment:
            idList.append(attachment.getId())

        return idList

    def __storeAttachment(self, attachmentPath, file_name: str):
        id = self.__database.insertAttachment(attachmentPath, file_name)
        return id

    def __findAttachment(self, attachementQuery):
        file = self.__database.findAttachent(attachementQuery)
        return file

    def __retrieveAttachment(self, attachmentID):
        file = self.__database.retrieveAttachment(attachmentID)
        return file

    def __findAttachment(self, query: dict):
        file = self.__database.findAttachment(query)
        return file
