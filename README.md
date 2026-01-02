# 学生信息管理系统

一个基于 Flask 的全栈 Web 应用，用于管理学生信息。

## 🌟 功能特性

- **学生信息管理**：增删改查（CRUD）操作
- **数据搜索**：支持学号、姓名、专业等多条件搜索
- **批量操作**：批量删除学生记录
- **数据导出**：一键导出为 Excel 文件
- **响应式设计**：适配手机、平板和电脑
- **表单验证**：前端与后端双重验证
- **分页显示**：大数据量下的分页浏览

## 🛠️ 技术栈

- **后端框架**：Flask (Python)
- **数据库**：SQLite + SQLAlchemy ORM
- **前端框架**：Bootstrap 5
- **表单处理**：Flask-WTF
- **数据导出**：Pandas + Openpyxl
- **前端图标**：Font Awesome

## 📁 项目结构

```
student_management/
├── app.py              # 主应用文件
├── models.py           # 数据库模型
├── forms.py            # 表单定义
├── config.py           # 配置文件
├── requirements.txt    # 依赖列表
├── README.md           # 项目说明（本文件）
├── .gitignore          # Git忽略配置
├── instance/           # 数据库文件（不上传）
├── templates/          # HTML模板
│   ├── base.html
│   ├── index.html
│   ├── add_student.html
│   └── edit_student.html
└── static/             # 静态资源
    ├── css/
    ├── js/
    └── images/
```

## 🚀 快速开始

### 环境要求
- Python 3.7+
- pip (Python包管理器)

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/student-management.git
cd student-management
```

2. **创建虚拟环境**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

4. **初始化数据库**
```bash
# 首次运行会自动创建数据库
python app.py
# 或手动初始化
python -c "from app import db; db.create_all()"
```

5. **运行项目**
```bash
python app.py
```

6. **访问项目**
浏览器打开 http://127.0.0.1:5000/

## 📸 项目截图

| 功能 | 截图描述 |
|------|----------|
| 学生列表 | 显示所有学生信息，支持搜索和分页 |
| 添加学生 | 表单页面，包含完整的数据验证 |
| 编辑学生 | 修改已有学生信息 |
| 批量操作 | 勾选多个学生进行批量删除 |
| 导出功能 | 一键导出 Excel 文件 |

## 🔧 配置说明

### 数据库配置
默认使用 SQLite 数据库，文件位于 `instance/students.db`

### 修改配置
编辑 `config.py` 文件：

```python
class Config:
    SECRET_KEY = 'your-secret-key-here'  # 生产环境请使用环境变量
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/students.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STUDENTS_PER_PAGE = 10
```

### 环境变量配置（生产环境推荐）
```bash
# Linux/Mac
export FLASK_SECRET_KEY='your-production-secret-key'
export FLASK_ENV='production'

# Windows
set FLASK_SECRET_KEY='your-production-secret-key'
set FLASK_ENV='production'
```

## 📊 API 接口

| 方法 | 端点 | 描述 | 示例 |
|------|------|------|------|
| GET | `/api/students` | 获取所有学生信息（JSON格式） | `curl http://localhost:5000/api/students` |

## 📝 使用示例

### 添加新学生
1. 点击导航栏"添加学生"按钮
2. 填写表单信息
3. 点击"保存学生信息"

### 搜索学生
1. 在搜索框输入关键词（学号、姓名、专业等）
2. 按回车或点击搜索按钮
3. 搜索结果实时显示

### 导出数据
1. 点击"导出Excel"按钮
2. 浏览器自动下载 Excel 文件
3. 使用 Excel 打开查看数据

### 批量操作
1. 勾选要操作的学生记录前的复选框
2. 选择"批量删除"操作
3. 确认删除操作

## 🐳 Docker 部署（可选）

```bash
# 构建镜像
docker build -t student-management .

# 运行容器
docker run -d -p 5000:5000 --name student-app student-management
```

## 🧪 测试

```bash
# 运行单元测试
python -m pytest tests/

# 运行特定测试文件
python -m pytest tests/test_models.py
```

## 🚀 生产环境部署

### 使用 Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用 Waitress (Windows)
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情

## 👨‍💻 作者

[你的名字] - [GitHub主页](https://github.com/your-username)

项目链接：https://github.com/your-username/student-management

## 🙏 致谢

- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Bootstrap 5 框架](https://getbootstrap.com/)
- [Font Awesome 图标库](https://fontawesome.com/)
- 所有贡献者和使用者

## ⚠️ 注意事项

1. **数据库文件**：`instance/students.db` 不应提交到版本控制
2. **密钥安全**：生产环境务必设置 `SECRET_KEY` 环境变量
3. **虚拟环境**：确保在虚拟环境中安装依赖
4. **文件权限**：确保应用有写入 `instance/` 目录的权限

## 🔄 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 实现基本 CRUD 功能
- 添加搜索和导出功能
- 响应式界面设计

---

**提示**：运行前请确保已激活虚拟环境并安装所有依赖。如有问题，请检查 Python 版本和依赖安装情况。
