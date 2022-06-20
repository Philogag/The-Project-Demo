import os
import time

import redis
from flask import Flask
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from backend.utility.config_helper import FlaskConfig
from backend.utility.json_encoder_helper import CustomJsonEncoder

"""
禁止全局引用backend中的函数
以免循环引用
"""

db = SQLAlchemy()

"""缓存"""
cache = Cache()

"""Redis"""
redis_client = redis.Redis()

"""Json Web Tokens"""
jwt = JWTManager()


def create_flask_app(
        flask_config: FlaskConfig,
):
    global db
    from backend.app_helper import (
        init_app_process,
        init_error_handler,
        process_before_request,
        init_logger
    )

    # 设置时区
    os.environ['TZ'] = flask_config.timezone
    try:
        time.tzset()
    except AttributeError:
        pass

    # 初始化日志
    init_logger(flask_config.logger.config_file)

    app = Flask(__name__)
    app.config.from_object(flask_config)
    app.app_context().push()  # for enable current_app

    # 增强Json编码器
    app.json_encoder = CustomJsonEncoder

    # 注入错误捕捉
    init_error_handler(app)

    # 初始化数据库
    app.config["SQLALCHEMY_DATABASE_URI"] = flask_config.db.get_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    db.init_app(app)

    # Load Redis.
    #

    # Load Login Manager.
    # from backend.utility.login_manager_helper import init_login_manager
    # init_login_manager(app)
    app.config["JWT_SECRET_KEY"] = flask_config.jwt.secret_key
    # app.config["JWT_TOKEN_LOCATION"] = flask_config.jwt.token_location
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = flask_config.jwt.access_token_expires
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = flask_config.jwt.refresh_token_expires
    # app.config["JWT_HEADER_NAME"] = flask_config.jwt.header_name
    # app.config["JWT_HEADER_TYPE"] = flask_config.jwt.header_type

    # app.config["JWT_BLACKLIST_ENABLED"] = config.jwt.blacklist_enabled
    # app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = config.jwt.blacklist_token_checks
    app.config["JWT_REDIS_BLOCKLIST"] = redis.StrictRedis(
        host=flask_config.redis.host,
        port=flask_config.redis.port,
        db=flask_config.redis.db,
        password=flask_config.redis.password,
        decode_responses=True,
    )
    jwt.init_app(app)

    # Load Blueprint.
    for file in os.listdir("./backend/blueprint"):
        if file.endswith("blueprint.py"):
            module = file[:-3]
            blueprint = getattr(
                __import__("backend.blueprint." + module, fromlist=True), module
            )
            app.register_blueprint(
                blueprint, url_prefix="/api/v1" + blueprint.url_prefix
            )

    # 初始化路由
    init_app_process(app)

    # 注入权限检查
    app.before_request(process_before_request)

    return app
