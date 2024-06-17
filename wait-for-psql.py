#!/usr/bin/env python3
import sys
import psycopg2
from urllib.parse import urlparse
from time import sleep

if __name__ == "__main__":
    url = urlparse(sys.argv[1])
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    while timeout > 0:
        try:
            conn = psycopg2.connect(
                dbname=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            conn.close()
            sys.exit(0)
        except psycopg2.OperationalError:
            timeout -= 1
            sleep(1)
    sys.exit(1)
