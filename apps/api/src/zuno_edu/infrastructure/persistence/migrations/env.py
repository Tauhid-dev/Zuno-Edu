"""Controlled migration job; never imported by API startup."""

import os

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.pool import NullPool
from zuno_edu.infrastructure.persistence.tables import metadata

url = make_url(os.environ["ZUNO_DATABASE_URL"])
if url.drivername != "postgresql+psycopg":
    raise ValueError("Migrations require an explicit PostgreSQL URL")

if context.is_offline_mode():
    context.configure(url=url, target_metadata=metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    engine = create_engine(url, poolclass=NullPool)
    try:
        with engine.connect() as connection:
            context.configure(connection=connection, target_metadata=metadata, compare_type=True)
            with context.begin_transaction():
                context.run_migrations()
    finally:
        engine.dispose()
