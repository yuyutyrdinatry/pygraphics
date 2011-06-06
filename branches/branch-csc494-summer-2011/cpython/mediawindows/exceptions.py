class MediaWindowsError(exceptions.Exception):
    """Generic error class for graphics module exceptions."""
    
    def __init__(self, args=None):
        '''Create an Error.'''
        
        self.args = args

# Error message strings
OBJ_ALREADY_DRAWN = "Object currently drawn"
UNSUPPORTED_METHOD = "Object doesn't support operation"
BAD_OPTION = "Illegal option value"
DEAD_THREAD = "Graphics thread quit unexpectedly"
