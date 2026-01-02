# models.py - 数据库模型
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

# 创建SQLAlchemy实例
db = SQLAlchemy()


class Student(db.Model):
    """
    学生数据模型
    对应数据库中的'students'表
    """
    # 表名
    __tablename__ = 'students'

    # 主键
    id = db.Column(db.Integer, primary_key=True)

    # 学号 - 唯一标识
    student_id = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True,
        comment='学生学号，唯一标识'
    )

    # 姓名
    name = db.Column(db.String(50), nullable=False, comment='学生姓名')

    # 年龄
    age = db.Column(db.Integer, nullable=False, comment='学生年龄')

    # 性别
    gender = db.Column(db.String(10), nullable=False, comment='性别')

    # 专业
    major = db.Column(db.String(100), nullable=False, comment='专业名称')

    # 邮箱
    email = db.Column(db.String(120), unique=True, nullable=False, comment='电子邮箱')

    # 电话（可选）
    phone = db.Column(db.String(20), nullable=True, comment='联系电话')

    # 地址（可选）
    address = db.Column(db.String(200), nullable=True, comment='家庭地址')

    # GPA成绩
    gpa = db.Column(db.Float, default=0.0, comment='平均绩点')

    # 入学日期
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow, comment='入学时间')

    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    # 更新时间
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment='最后更新时间'
    )

    # 数据验证
    @validates('email')
    def validate_email(self, key, email):
        """验证邮箱格式"""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('邮箱格式无效')
        return email

    @validates('student_id')
    def validate_student_id(self, key, student_id):
        """验证学号格式"""
        if not re.match(r'^[A-Za-z0-9]{6,20}$', student_id):
            raise ValueError('学号必须为6-20位字母或数字')
        return student_id

    def __repr__(self):
        """对象的字符串表示"""
        return f'<Student {self.student_id}: {self.name}>'

    def to_dict(self):
        """转换为字典，用于API或导出"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'major': self.major,
            'email': self.email,
            'phone': self.phone or '',
            'address': self.address or '',
            'gpa': f'{self.gpa:.2f}',
            'enrollment_date': self.enrollment_date.strftime('%Y-%m-%d')
            if self.enrollment_date else '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def get_gpa_level(self):
        """获取GPA等级"""
        if self.gpa >= 3.5:
            return '优秀'
        elif self.gpa >= 2.5:
            return '良好'
        elif self.gpa >= 1.5:
            return '及格'
        else:
            return '不及格'