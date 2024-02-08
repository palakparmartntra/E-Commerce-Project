

class FormRegex:
    EMAIL_REGEX = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    ZIPCODE_REGEX = r'^[0-9]{6}$'
    NAME = '^[a-zA-Z]+$'
    PHONE_NO = r'^\d{10}$'