"""Fresh PostgreSQL upgrade, metadata drift, data-preserving app rollback."""

from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from zuno_edu.bootstrap.app import create_app
from zuno_edu.infrastructure.persistence.database import Database

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.migration


def test_initial_migration_upgrade_and_compatibility(database_url: str) -> None:
    config = Config(str(ROOT / "alembic.ini"))
    database = Database(database_url)
    try:
        assert sa.inspect(database.engine).get_table_names() == []
        create_app()  # API startup never creates tables.
        assert sa.inspect(database.engine).get_table_names() == []
        command.upgrade(config, "head")
        assert set(sa.inspect(database.engine).get_table_names()) == {
            "alembic_version",
            "outbox_events",
            "background_jobs",
            "webhook_inbox",
        }
        command.check(config)
        command.upgrade(config, "head")
        # C01's API remains compatible with the expanded schema (application rollback).
        from fastapi.testclient import TestClient

        with TestClient(create_app()) as client:
            assert client.get("/api/v1/health").status_code == 200
        with pytest.raises(RuntimeError, match="Data-preserving"):
            command.downgrade(config, "base")
        with database.engine.connect() as connection:
            assert connection.scalar(sa.text("SELECT version_num FROM alembic_version")) == "0001"
    finally:
        database.close()
