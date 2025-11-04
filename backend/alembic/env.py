from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import Connection
import asyncio
import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from core.models.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.


# Ensure backend directory is on PYTHONPATH so `core` imports resolve
here = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(here, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine. SQL will be emitted as strings.
    """
    url = settings.db.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an AsyncEngine."""
    connectable = create_async_engine(
        settings.db.url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:  # type: Connection
        await connection.run_sync(_do_run_migrations)


def _do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection,
                      target_metadata=target_metadata, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
