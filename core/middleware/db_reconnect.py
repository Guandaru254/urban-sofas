# core/middleware/db_reconnect.py
"""
Middleware to automatically reconnect the database
when a connection is lost due to timeout or network issues.
Useful for Render or other ephemeral DB connections.
"""

import logging
from django.db import connections
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)


class DBReconnectMiddleware:
    """
    Attempts to reconnect to the database if a connection error occurs.
    Should be placed near the top of the MIDDLEWARE list.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Test the connection before processing the request
            for conn in connections.all():
                conn.cursor()
        except OperationalError:
            logger.warning("Lost database connection. Attempting to reconnect...")
            for conn in connections.all():
                conn.close_if_unusable_or_obsolete()

        response = self.get_response(request)
        return response
