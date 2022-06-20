import logging

from flask_script import Command

from .generate_basic_menu import GenerateBasicMenu
from .generate_super_user import GenerateSuperUser
from .generate_system_robots import GenerateSystemRobots
from .generate_system_roles import GenerateSystemRoles


class InitDatabaseData(Command):
    @classmethod
    def run(cls):
        commands = [
            GenerateSystemRobots,
            GenerateSystemRoles,
            GenerateBasicMenu,
            GenerateSuperUser,
        ]
        for command in commands:
            logging.info("Run: " + command.__name__)
            command.run()
            logging.info(command.__name__ + "Done.")
