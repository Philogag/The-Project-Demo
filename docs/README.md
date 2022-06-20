

# 开发手册

### alembic工具（数据库版本控制）

```bash
# 自动生成更新sql
alembic revision --autogenerate -m "此处填写更新备注"
# 更新数据库到最新状态
alembic upgrade head
```