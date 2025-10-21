# Odoo Custom Module Deployment (Railway)

This project deploys an Odoo 17 server with a custom module using Docker on Railway.

## Deployment Steps

1. Push this repo to GitHub.
2. Create a PostgreSQL database (free):
   - [Neon.tech](https://neon.tech) or [ElephantSQL](https://www.elephantsql.com)
   - Copy the connection details.
3. Go to [Railway](https://railway.app):
   - New Project → Deploy from GitHub → Select this repo.
   - Add environment variables (DB credentials) in the Variables tab:
     ```
     DB_HOST=...
     DB_PORT=5432
     DB_USER=...
     DB_PASSWORD=...
     DB_NAME=...
     ```
4. Railway builds and deploys automatically.
5. Visit your Railway app URL.
6. Complete Odoo setup → go to Apps → Update Apps List → Install your custom module.
