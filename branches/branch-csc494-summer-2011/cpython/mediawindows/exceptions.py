class MediaWindowsError(Exception):
    """Generic error class for graphics module exceptions."""
    pass

class WindowDoesNotExistError(MediaWindowsError):
    """Error class for when an attempt is made to manipulate a closed window"""
    pass

# Error message strings
OBJ_ALREADY_DRAWN = "Object currently drawn"
UNSUPPORTED_METHOD = "Object doesn't support operation"
BAD_OPTION = "Illegal option value"
DEAD_THREAD = "Graphics thread quit unexpectedly"
