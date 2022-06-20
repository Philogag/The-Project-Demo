import os
import sys

root = os.path.dirname(__file__) + "/../"  # 定位到project根目录
sys.path.append(root)

from flask_script import Manager

from backend.app_entry import flask_app
from backend.script import *

manager = Manager(flask_app)

manager.add_command("init_db", init_db.InitDatabaseData)
manager.add_command("generate_system_robots", generate_system_robots.GenerateSystemRobots)
manager.add_command("generate_system_roles", generate_system_roles.GenerateSystemRoles)
manager.add_command("generate_super_user", generate_super_user.GenerateSuperUser)
manager.add_command("generate_basic_menu", generate_basic_menu.GenerateBasicMenu)
manager.add_command("generate_area", generate_area.GenerateArea)

if __name__ == "__main__":
    manager.run()
