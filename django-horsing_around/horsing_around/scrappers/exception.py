class PageDoesNotExist(Exception):
    def __init__(self, message):
        super(PageDoesNotExist, self).__init__(message)
