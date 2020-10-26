from enum import Enum

class FindingType(str, Enum):
    CREDENTIALS_COMPLEXITY: str = "Credentials Complexity"
    MANUFACTURER_DEFAULT_CREDS: str = "Manufacturer Default Creds"
    LACK_OF_AUTHENTICATION: str = "Lack Of Authentication"
    PLAIN_TEXT_PROTOCOLS: str = "Plain Text Protocols"
    PLAIN_TEXT_WEB_LOGIN: str = "Plain Text Web Login"
    ENCRYPTION: str = "Encryption"
    AUTHENTICATION_BYPASS: str = "Authentication Bypass"
    PORT_SECURITY: str = "Port Security"
    ACCESS_CONTROL: str = "Access Control"
    LEAST_PRIVILEGE: str = "Least Privilege"
    PRIVILEGE_ESCALATION: str = "Privilege Escalation"
    MISSING_PATCHES: str = "Missing Patches"
    PHYSICAL_SECURITY: str = "Physical Security"
    INFORMATION_DISCLOSURE: str = "Information Disclosure"

    @staticmethod
    def getMember(value: str):
        for member in FindingType:
            if member.value == value:
                return member