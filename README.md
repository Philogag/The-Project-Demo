# TheProject

基于 Flask + Vue(VBen-Admin) 的中台系统模板

+ 基于角色+用户的权限分发与管理
+ 前后独立的路由权限配置（视图权限+数据权限）
+ 基于 Sqlalchemy 的 Orm 数据操作模式
+ 基于 Redis 的高频数据缓存


# 开发环境

### 1. postgresql 数据库

```sql
create user 用户名 with password '密码';
create database 数据库名 owner 用户名;
GRANT ALL PRIVILEGES ON DATABASE 数据库名 TO 用户名;
```

### 2. python 环境

+ python 3.9.9

```bash
$: python -m venv .venv
$: .venv/Scripts/activate
$: pip install -r requirements.txt
```

将 backend 文件夹中 `app.development.toml.template` 文件 更名为 `app.development.toml` 并编辑内部数据库配置

> 使用 vscode 打开项目文件夹  
> 打开 项目内 任意 python 文件  
> 右下角选择 python 解释器为 带venv项



### 3. 数据库初始化
```bash
$: alembic revision --autogenerate -m "init"  # 解析 entity 并生成sql
$: alembic upgrade head  # 应用最新更改到数据库
$: python backend/script.py init_db # 创建机器人、超级管理员等基本信息
```

> 备注：  
> +  由于 flask_script 库版本原因，该库会报错
> 
>     ModuleNotFoundError: No module named 'flask._compat'
> 
> 只需将 .venv\lib\site-packages\flask_script\__init__.py 文件中第15行的
> `from flask._compat import` 改为 `from ._compat import` 后重新运行即可

### 4. 前端开发环境(nodejs)
+ nodejs 最新稳定版即可

```bash
$: npm install yarn -g
$: cd frontend/desktop
$: yarn install
```

### 5. 启动前后端开发服务器
vscode 打开 `运行与调试` 切换到 `Run All DevServer` 按 F5 双端即可正常启动