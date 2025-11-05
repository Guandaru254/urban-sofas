from django.db import connection, OperationalError, InterfaceError

class DBReconnectMiddleware:
    """Ensures a working DB connection before each request (Render sleep fix)"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            connection.ensure_connection()
        except (OperationalError, InterfaceError):
            connection.close()
            connection.connect()
        return self.get_response(request)
