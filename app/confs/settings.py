from functools import lru_cache
from prettyconf import config


class BaseConfig:
    APP_DEBUG = config("DEBUG",
        default=False, cast=config.boolean
    )

    APP_ENVIRONMENT = config("APP_ENVIRONMENT",
        default="tests", cast=str
    )

    APP_HOST = config("APP_HOST",
        default="127.0.0.1", cast=str
    )

    APP_HOST_PORT = config("APP_HOST_PORT",
        default="8000", cast=str
    )

    APP_PREFIX = config("APP_PREFIX",
        default="", cast=str
    )

    DATABASE_PORT = config("DATABASE_PORT",
        default="5432", cast=str
    )

    DATABASE_HOST = config("DATABASE_HOST",
        default="", cast=str
    )

    DATABASE_NAME = config("DATABASE_NAME",
        default="", cast=str
    )

    DATABASE_PARAMETERS = config("DATABASE_PARAMETERS",
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
