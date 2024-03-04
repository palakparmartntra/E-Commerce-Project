

class CannotDeleteBrandException(Exception):
    """ Raised when brand has products """


class PriorityNotUniqueException(Exception):
    """ Raised when the priority of a section is not unique """


class InvalidFileTypeException(Exception):
    """ Raised when the file type is invalid """
