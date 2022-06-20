import random
import re
import string
import uuid


def generate_random_string(
    length=8, chars=string.ascii_letters + string.ascii_uppercase + string.digits
) -> str:
    return "".join(random.choices(chars, k=length))


def generate_uuid_id():
    return str(uuid.uuid4())


uuid_pattern = re.compile(r"^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}$")


def is_fake_uuid(text: string):
    return not text or not re.match(uuid_pattern, text)


def is_blank(content: str) -> bool:
    """
    :return: `True` if string is total blank.
    """
    return not (content and content.strip())


def name_camel_to_underline(value: str, split_number: bool = True):
    """
    驼峰命名转下划线命名
    :params split_number: 数字是否独立分区，default: True
    """
    result = re.sub(r'(.*?)([A-Z])', r'\1_\2', value).lower()
    if split_number:
        result = re.sub(r'(.*?)([0-9]+)(.*?)', r'\1_\2_\3', result)
    return result


def name_underline_to_camel(value: str):
    """
    下划线命名转驼峰
    """
    splits = value.split("_")
    return splits[0].lower() + "".join([s.capitalize() for s in splits[1:]])
