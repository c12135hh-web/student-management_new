# forms.py - 表单定义
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, Optional


class StudentForm(FlaskForm):
    """
    学生信息表单
    用于添加和编辑学生信息
    """

    # 学号字段
    student_id = StringField('学号', validators=[
        DataRequired(message='学号不能为空'),
        Length(min=6, max=20, message='学号长度6-20位'),
        Regexp('^[A-Za-z0-9]+$', message='学号只能包含字母和数字')
    ], render_kw={
        "placeholder": "例如: 20230001",
        "class": "form-control"
    })

    # 姓名字段
    name = StringField('姓名', validators=[
        DataRequired(message='姓名不能为空'),
        Length(min=2, max=50, message='姓名长度2-50位')
    ], render_kw={
        "placeholder": "请输入学生姓名",
        "class": "form-control"
    })

    # 年龄字段
    age = IntegerField('年龄', validators=[
        DataRequired(message='年龄不能为空'),
        NumberRange(min=10, max=60, message='年龄范围10-60岁')
    ], render_kw={
        "placeholder": "例如: 18",
        "class": "form-control",
        "min": "10",
        "max": "60"
    })

    # 性别字段
    gender = SelectField('性别', choices=[
        ('', '请选择性别'),
        ('男', '男'),
        ('女', '女'),
        ('其他', '其他')
    ], validators=[DataRequired(message='请选择性别')], render_kw={
        "class": "form-select"
    })

    # 专业字段
    major = StringField('专业', validators=[
        DataRequired(message='专业不能为空'),
        Length(max=100, message='专业不超过100字')
    ], render_kw={
        "placeholder": "例如: 计算机科学与技术",
        "class": "form-control"
    })

    # 邮箱字段
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='请输入有效的邮箱地址'),
        Length(max=120, message='邮箱不超过120字符')
    ], render_kw={
        "placeholder": "example@university.edu.cn",
        "class": "form-control",
        "type": "email"
    })

    # 电话字段
    phone = StringField('电话', validators=[
        Optional(),
        Length(max=20, message='电话不超过20位'),
        Regexp(r'^[0-9+\-\s()]*$', message='请输入有效的电话号码')
    ], render_kw={
        "placeholder": "13800138000",
        "class": "form-control"
    })

    # 地址字段
    address = TextAreaField('地址', validators=[
        Optional(),
        Length(max=200, message='地址不超过200字')
    ], render_kw={
        "placeholder": "例如: 北京市海淀区中关村大街",
        "class": "form-control",
        "rows": "3"
    })

    # GPA字段
    gpa = FloatField('GPA', validators=[
        Optional(),
        NumberRange(min=0.0, max=4.0, message='GPA范围0.0-4.0')
    ], render_kw={
        "placeholder": "0.0-4.0",
        "class": "form-control",
        "step": "0.01",
        "min": "0.0",
        "max": "4.0"
    })