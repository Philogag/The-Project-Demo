from functools import wraps

import jsonpickle

from backend.factory import redis_client


def redis_cached(expired_seconds: int = 180):
    """
    redis缓存装饰器
    :param expired_seconds:
    :return:
    """

    def __actual_redis_cached(func):
        def __generate_list_args_token(__args_list) -> str:
            result_list = []
            for __args in __args_list:
                result_list.append(str(__args))
            return ",".join(result_list)

        def __generate_dict_args_list(__args_dict) -> str:
            result_list = []
            for key, value in __args_dict.items():
                result_list.append("{0}={1}".format(key, value))
            return ",".join(result_list)

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = "cached:{0}:{1},{2}".format(
                func.__name__,
                __generate_list_args_token(args),
                __generate_dict_args_list(kwargs),
            )
            redis_helper_instance = redis_client
            redis_result = redis_helper_instance.get(key=cache_key)

            if redis_result is None:
                value = func(*args, **kwargs)
                value_json = jsonpickle.encode(value)
                redis_helper_instance.set(
                    key=cache_key, value=value_json, expired_seconds=expired_seconds
                )
            else:
                value = jsonpickle.decode(redis_result)
            return value

        return wrapper

    return __actual_redis_cached
