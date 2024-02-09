
class FormRegex:
    EMAIL = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    ZIPCODE = r'^[0-9]{6}$'
    NAME = '^[A-Za-z]+\s?([A-Za-z]+)?$'
    PHONE_NO = r'^\d{10}$'
