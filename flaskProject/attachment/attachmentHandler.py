from flaskProject.attachment.attachment import Attachment
from flaskProject.database.databaseHandler import DatabaseHandler

class AttachmentHandler:
    def __init__(self, attachment_ids: list = []):
        self.__attachment: list = []
        self.__database = DatabaseHandler()
        self.__getAttachments(attachment_ids)

    def find_attachment(self, file_name: str):
        for item in self.__attachment:
            if self.__attachment.getFileName() == file_name:
                return item
        return None

    def find_and_open_attachment(self, file_name: str):
        for item in self.__attachment:
            if item.getFileName() == file_name:
                item.viewFile()

    # This algorithm attempts to create an instance of Attachment that has at type 'gridfs.grid_file.GridOut'
    # as the attachment argument. This type allows the attachment to be treated as a file,
    # while also giving access to aditional meta data that was stored.

    def appendAttachment(self, path, attachment_name: str =""):
        id = self.__database.storeAttachment(path, file_name=attachment_name)
        file = self.__database.retrieveAttachment(id)
        self.__attachment.append(Attachment(attachment=file, file_name = attachment_name, _id= id))

    def __getAttachments(self, attachment_id: list):
        for id in attachment_id:
            attachment_data = self.__database.retrieveAttachment(id)
            self.__attachment.append(Attachment(attachment= attachment_data
                                                , file_name=attachment_data.filename
                                                , _id= attachment_data._id))
