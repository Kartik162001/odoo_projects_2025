# Use official Odoo 17 image
FROM odoo:17.0

# Copy custom modules
COPY ./addons /mnt/extra-addons

# Install optional Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt || true

# Expose Odoo default port
EXPOSE 8069

# Start Odoo with standard and custom addons
CMD ["odoo", "--addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons"]
