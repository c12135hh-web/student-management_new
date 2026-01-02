# config.py - 配置文件
import os

# 获取项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 安全密钥（在生产环境中应该从环境变量读取）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2024'

    # SQLite数据库路径
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'students.db')

    # 关闭SQLAlchemy事件系统，节省内存
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 分页设置
    STUDENTS_PER_PAGE = 10

    # 调试模式设置（开发时启用）
    DEBUG = True


# 创建配置实例
config = Config()