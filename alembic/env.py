from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 👇 Импортируем Base и модели, чтобы Alembic знал о них
from app.database import Base
from app.models import rooms  # <-- ОБЯЗАТЕЛЕН, даже если не используешь явно

# Получаем конфиг Alembic из alembic.ini
config = context.config

# Конфигурируем логгеры (если есть logging.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем metadata проекта
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Запуск миграций в offline-режиме (без подключения к базе).
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Запуск миграций в online-режиме (с подключением к базе).
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
