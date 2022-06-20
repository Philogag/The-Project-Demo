"""
入口
"""
import os, sys

root = os.path.dirname(__file__) + "/../"  # 定位到project根目录
sys.path.append(root)

from backend.factory import create_flask_app
from backend.utility.config_helper import load_config_from_toml


def __get_abs_path(path_str: str):
    folder, _ = os.path.split(os.path.abspath(__file__))
    return os.path.join(folder, path_str)


app_config_toml = os.getenv('FLASK_CONFIG_TOML')
app_config_toml = app_config_toml if app_config_toml else __get_abs_path("app.development.toml")

flask_app = create_flask_app(load_config_from_toml(app_config_toml))

if __name__ == "__main__":
    flask_app.run(debug=True)
