from functools import lru_cache
from prettyconf import config


class BaseConfig:
    APP_HOST = config("APP_HOST",
        default="127.0.0.1", cast=str
    )

    APP_PORT = config("APP_PORT",
        default=8000, cast=int
    )

    APP_PREFIX = config("APP_PREFIX",
        default="", cast=str
    )

    APP_DEBUG = config("DEBUG",
        default=False, cast=config.boolean
    )

    APP_ENVIRONMENT = config("APP_ENVIRONMENT",
        default="tests", cast=str
    )

    DATABASE_HOST = config("DATABASE_HOST",
        default="127.0.0.1", cast=str
    )

    DATABASE_PORT = config("DATABASE_PORT",
        default=5432, cast=int
    )

    DATABASE_NAME = config("DATABASE_NAME",
        default="", cast=str
    )

    DATABASE_PARAMETERS = config("DATABASE_PARAMETERS",
        default="", cast=str
    )

    DATABASE_USER = config("DATABASE_USER",
        default="", cast=str
    )

    DATABASE_PASSWORD = config("DATABASE_PASSWORD",
        default="", cast=str
    )

    STORAGE_HOST = config("STORAGE_HOST",
        default="127.0.0.1", cast=str
    )

    STORAGE_PORT = config("STORAGE_PORT",
        default=9000, cast=int
    )

    STORAGE_USER = config("STORAGE_USER",
        default="", cast=str
    )

    STORAGE_PASSWORD = config("STORAGE_PASSWORD",
        default="", cast=str
    )

    STORAGE_NAME = config("STORAGE_NAME",
        default="", cast=str
    )

    STORAGE_SERVICE_NAME = config("STORAGE_SERVICE_NAME",
        default="", cast=str
    )

    MESSAGE_BROKER_PORT = config("MESSAGE_BROKER_PORT",
        default=5672, cast=int
    )

    MESSAGE_BROKER_HOST = config("MESSAGE_BROKER_HOST",
        default="127.0.0.1", cast=str
    )

    MESSAGE_BROKER_PASSWORD = config("MESSAGE_BROKER_PASSWORD",
        default="", cast=str
    )

    MESSAGE_BROKER_USER = config("MESSAGE_BROKER_USER",
        default="", cast=str
    )

    JWT_SECRET = config("JWT_SECRET",
        default="", cast=str
    )

    JWT_ALGORITHM = config("JWT_ALGORITHM",
        default="HS256", cast=str
    )


class ProductionConfig(BaseConfig):
    ...


class StagingConfig(BaseConfig):
    ...


class DevelopmentConfig(BaseConfig):
    ...


class TestsConfig(BaseConfig):
    DATABASE_NAME = f"{BaseConfig.DATABASE_NAME}_tests"


@lru_cache
def get_environment_settings() -> BaseConfig:
    config_cls_dict = {
        "production": ProductionConfig, "staging": StagingConfig, "development": DevelopmentConfig, "tests": TestsConfig
    }

    return config_cls_dict[
        str(BaseConfig.APP_ENVIRONMENT).lower()
    ]()


settings = get_environment_settings()
