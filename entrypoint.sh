#!/bin/bash

ls -l /  # Asegúrate de que el script esté presente en la raíz del contenedor
/wait-for-psql.py db --timeout=30 -- echo "PostgreSQL is ready."
exec "$@"
