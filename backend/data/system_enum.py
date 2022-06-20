from enum import Enum

from backend.model.edit.master_user_em import MasterUserEm
from backend.model.edit.robot_em import RobotEm
from backend.model.edit.role_em import RoleEm


class EnumKeyNameRule(Enum):
    """"""
    underline = "下划线命名"
    camel = "驼峰命名"


class EnumHandlerCategory(Enum):
    """
    事件发起人对应实体
    category: model_name
    """

    master_user = MasterUserEm.__name__
    role = RoleEm.__name__
    system_robot = RobotEm.__name__


class EnumDataPermissionCategory(Enum):
    """
    授权类别
    """
    allow = "允许"
    allow_all = "允许所有"


class EnumRoleCode(Enum):
    """
    角色类别
    code: name
    """

    guest = "游客"
    super_admin = "系统管理员"
    test = "测试"
    admin = "组织管理员"


class EnumRobotCode(Enum):
    """
    机器人类别
    code: name
    """

    init_robot = "系统初始化机器人"
    message_queue_robot = "消息队列机器人"
    cron_robot = "定时任务机器人"


class EnumRouteCategory(Enum):
    data = "后端路由（数据路由）"
    view = "前端路由（页面路由）"

