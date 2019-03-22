from contextlib import contextmanager

from psycopg2.pool import ThreadedConnectionPool


class ConnectionManager:
    def __init__(self, minconn, maxconn, connection_args):
        self.pool = ThreadedConnectionPool(minconn, maxconn, **connection_args)

    @contextmanager
    def connect(self):
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)
