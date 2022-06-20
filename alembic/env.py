import os, sys

root = os.path.dirname(__file__)+'/../'  # 定位到project根目录
sys.path.append(root)

import logging
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from backend.utility.config_helper import load_config_from_toml

# from backend.app_entry import flask_app

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

app_config_toml = os.getenv('FLASK_CONFIG_TOML')
app_config_toml = app_config_toml if app_config_toml else "./backend/app.development.toml"
flask_config = load_config_from_toml(app_config_toml)
config.set_main_option('sqlalchemy.url', flask_config.db.get_uri())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from backend.data.unit_of_work import UnitOfWorkEntity
from backend.model.entity import scan_all_entities

entities = [
    UnitOfWorkEntity,
    *scan_all_entities(),
]

logging.info(", ".join(map(lambda x: x.__name__, entities)))
target_metadata = set(cls.metadata for cls in entities)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
