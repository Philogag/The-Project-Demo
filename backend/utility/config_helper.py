import os
from typing import Optional, Union

import toml
from pydantic import BaseModel

from backend.utility.error_helper import BusinessError


class DevConfig(BaseModel):
    debug = True


class LoggerConfig(BaseModel):
    config_file: str


class DatabaseConfig(BaseModel):
    type: Optional[str]
    host: str
    port: Union[int, str]
    db: str
    username: str
    password: str

    def get_uri(self):
        return f"{self.type}://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"


class RedisConfig(BaseModel):
    host: str
    port: Union[int, str]
    db: int
    password: str


class JWTConfig(BaseModel):
    secret_key: str = "jwt-secret-key_"
    token_location: str = ''
    access_token_expires: int
    refresh_token_expires: int


class FlaskConfig(BaseModel):
    app_name: str

    secret_key: str
    timezone: str = "Asia/Shanghai"

    db: DatabaseConfig
    redis: RedisConfig
    jwt: JWTConfig
    logger: LoggerConfig


def load_config_from_toml(filepath) -> FlaskConfig:
    if os.path.isfile(filepath):
        config_dict = toml.load(filepath)
        return FlaskConfig(**config_dict)
    else:
        raise BusinessError("配置文件不存在")
