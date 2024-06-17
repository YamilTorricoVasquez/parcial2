FROM odoo:17.0

# Copiar los archivos de configuración
COPY ./entrypoint.sh /
COPY ./config_odoo/odoo.conf /etc/odoo/
# Copiar el script para esperar a PostgreSQL
COPY wait-for-psql.py /wait-for-psql.py
USER root
RUN chmod +x /entrypoint.sh \
    && chmod +x /wait-for-psql.py \
    && chown odoo:odoo /etc/odoo/odoo.conf \
    && mkdir -p /mnt/extra-addons \
    && chown -R odoo:odoo /mnt/extra-addons \
    && mkdir -p /var/log/odoo \
    && chown -R odoo:odoo /var/log/odoo

# Exponer Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

# Copiar el script para esperar a PostgreSQL
COPY wait-for-psql.py /usr/local/bin/wait-for-psql.py

# Establecer el usuario predeterminado al ejecutar el contenedor
USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]
