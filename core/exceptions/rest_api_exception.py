class RestApiException(Exception):
    """Generic exception for rest api"""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return "/!\\ REST API EXCEPTION: " + self.message
