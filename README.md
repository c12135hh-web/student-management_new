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
student_management/
├── app.py # 主应用文件
├── models.py # 数据库模型
├── forms.py # 表单定义
├── config.py # 配置文件
├── requirements.txt # 依赖列表
├── README.md # 项目说明（本文件）
├── .gitignore # Git忽略配置
├── instance/ # 数据库文件（不上传）
├── templates/ # HTML模板
│ ├── base.html
│ ├── index.html
│ ├── add_student.html
│ └── edit_student.html
└── static/ # 静态资源
├── css/
├── js/
└── images/

## 🚀 快速开始

### 环境要求
- Python 3.7+
- pip (Python包管理器)

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/你的用户名/student-management.git
cd student-management
2. **创建虚拟环境**
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. **安装依赖**
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
4. **运行项目**
python app.py
5. **访问项目**
浏览器打开 http://127.0.0.1:5000/
📸 项目截图
功能	截图描述
学生列表	显示所有学生信息，支持搜索和分页
添加学生	表单页面，包含完整的数据验证
编辑学生	修改已有学生信息
批量操作	勾选多个学生进行批量删除
导出功能	一键导出 Excel 文件
🔧 配置说明
数据库配置
默认使用 SQLite 数据库，文件位于 instance/students.db

修改配置
编辑 config.py 文件：
class Config:
    SECRET_KEY = 'your-secret-key-here'  # 生产环境请使用环境变量
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/students.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STUDENTS_PER_PAGE = 10
📊 API 接口
方法	端点	描述	示例
GET	/api/students	获取所有学生信息（JSON格式）	curl http://localhost:5000/api/students
📝 使用示例
添加新学生
点击导航栏"添加学生"按钮

填写表单信息

点击"保存学生信息"

搜索学生
在搜索框输入关键词（学号、姓名、专业等）

按回车或点击搜索按钮

搜索结果实时显示

导出数据
点击"导出Excel"按钮

浏览器自动下载 Excel 文件

使用 Excel 打开查看数据

🤝 贡献指南
Fork 本仓库

创建功能分支 (git checkout -b feature/AmazingFeature)

提交更改 (git commit -m 'Add some AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

开启 Pull Request

📄 许可证
本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情

👨‍💻 作者
你的名字 - GitHub主页

项目链接：https://github.com/你的用户名/student-management

🙏 致谢
Flask 官方文档

Bootstrap 5 框架

Font Awesome 图标库

所有贡献者和使用者

### 步骤3：清理不需要的文件
删除或确保以下文件不会被提交：
```bash
# 确保这些不会上传：
- instance/students.db（数据库文件）
- .venv/ 或 venv/（虚拟环境）
- __pycache__/（缓存文件）
- 任何调试文件