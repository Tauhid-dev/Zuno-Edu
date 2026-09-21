"""Real PostgreSQL only, isolated database per test; never touch a default database."""

import os
from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from sqlalchemy.engine import make_url
from zuno_edu.infrastructure.persistence.database import Database

ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture
def database_url(monkeypatch: pytest.MonkeyPatch) -> Iterator[str]:
    raw = os.environ.get("ZUNO_TEST_DATABASE_URL")
    if not raw:
        pytest.fail("ZUNO_TEST_DATABASE_URL must identify an isolated PostgreSQL test server")
    url = make_url(raw)
    if url.host not in ("127.0.0.1", "localhost") or url.database != "zuno_c02_test":
        pytest.fail("Refusing a non-local or non-disposable test database")
    name = f"zuno_c02_{uuid4().hex}"
    admin = sa.create_engine(url, isolation_level="AUTOCOMMIT")
    with admin.connect() as connection:
        connection.execute(sa.text(f'CREATE DATABASE "{name}"'))
    test_url = url.set(database=name).render_as_string(hide_password=False)
    monkeypatch.setenv("ZUNO_DATABASE_URL", test_url)
    try:
        yield test_url
    finally:
        with admin.connect() as connection:
            connection.execute(sa.text(f'DROP DATABASE "{name}" WITH (FORCE)'))
        admin.dispose()


@pytest.fixture
def db(database_url: str) -> Iterator[Database]:
    command.upgrade(Config(str(ROOT / "alembic.ini")), "head")
    database = Database(database_url)
    try:
        yield database
    finally:
        database.close()
