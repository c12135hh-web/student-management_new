# app.py - 主应用文件
import os
import sys
from datetime import datetime
from io import BytesIO

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_file, jsonify, abort
)
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 导入配置和模型
from config import config
from models import db, Student
from forms import StudentForm


def create_app():
    """应用工厂函数"""
    # 创建Flask应用
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config)

    # 确保instance文件夹存在
    instance_path = os.path.join(app.root_path, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print(f"创建目录: {instance_path}")

    # 初始化数据库
    db.init_app(app)

    # 创建数据库表
    with app.app_context():
        db.create_all()
        print("数据库初始化完成!")

    return app


# 创建应用实例
app = create_app()


# ==================== 辅助函数 ====================

def get_pagination_params():
    """获取分页参数"""
    page = request.args.get('page', 1, type=int)
    per_page = app.config.get('STUDENTS_PER_PAGE', 10)
    return page, per_page


def get_search_query():
    """获取搜索查询"""
    search = request.args.get('search', '', type=str).strip()
    return search


def build_search_filter(query, search_term):
    """构建搜索过滤器"""
    if search_term:
        search_filter = db.or_(
            Student.name.contains(search_term),
            Student.student_id.contains(search_term),
            Student.major.contains(search_term),
            Student.email.contains(search_term)
        )
        query = query.filter(search_filter)
    return query


# ==================== 路由定义 ====================

@app.route('/')
def index():
    """首页 - 显示学生列表"""
    try:
        # 获取参数
        page, per_page = get_pagination_params()
        search = get_search_query()

        # 构建查询
        query = Student.query

        # 应用搜索过滤器
        query = build_search_filter(query, search)

        # 执行分页查询
        students = query.order_by(Student.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # 计算统计信息
        total_students = Student.query.count()
        male_count = Student.query.filter_by(gender='男').count()
        female_count = Student.query.filter_by(gender='女').count()

        return render_template(
            'index.html',
            students=students,
            search=search,
            total_students=total_students,
            male_count=male_count,
            female_count=female_count
        )

    except Exception as e:
        app.logger.error(f"加载首页时出错: {str(e)}")
        flash('加载数据时发生错误，请稍后重试', 'danger')
        abort(500)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """添加新学生"""
    form = StudentForm()

    if form.validate_on_submit():
        try:
            # 检查学号是否已存在
            existing = Student.query.filter_by(
                student_id=form.student_id.data
            ).first()

            if existing:
                flash('该学号已存在，请使用其他学号', 'danger')
                return render_template('add_student.html', form=form)

            # 检查邮箱是否已存在
            existing_email = Student.query.filter_by(
                email=form.email.data
            ).first()

            if existing_email:
                flash('该邮箱已被注册，请使用其他邮箱', 'danger')
                return render_template('add_student.html', form=form)

            # 创建新学生
            student = Student(
                student_id=form.student_id.data,
                name=form.name.data,
                age=form.age.data,
                gender=form.gender.data,
                major=form.major.data,
                email=form.email.data,
                phone=form.phone.data or None,
                address=form.address.data or None,
                gpa=form.gpa.data or 0.0,
                enrollment_date=datetime.utcnow()
            )

            # 保存到数据库
            db.session.add(student)
            db.session.commit()

            flash(f'学生 {student.name} 添加成功！', 'success')
            return redirect(url_for('index'))

        except ValueError as e:
            db.session.rollback()
            flash(f'数据验证失败: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"添加学生失败: {str(e)}")
            flash('添加学生失败，请检查数据格式', 'danger')

    return render_template('add_student.html', form=form)


@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    """编辑学生信息"""
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)

    if form.validate_on_submit():
        try:
            # 检查学号是否与其他学生冲突
            if form.student_id.data != student.student_id:
                existing = Student.query.filter_by(
                    student_id=form.student_id.data
                ).first()
                if existing and existing.id != student.id:
                    flash('该学号已被其他学生使用', 'danger')
                    return render_template('edit_student.html', form=form, student=student)

            # 检查邮箱是否与其他学生冲突
            if form.email.data != student.email:
                existing = Student.query.filter_by(
                    email=form.email.data
                ).first()
                if existing and existing.id != student.id:
                    flash('该邮箱已被其他学生使用', 'danger')
                    return render_template('edit_student.html', form=form, student=student)

            # 更新学生信息
            form.populate_obj(student)
            db.session.commit()

            flash(f'学生 {student.name} 信息更新成功！', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"更新学生失败: {str(e)}")
            flash('更新学生信息失败', 'danger')

    return render_template('edit_student.html', form=form, student=student)


@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """删除学生"""
    student = Student.query.get_or_404(student_id)
    student_name = student.name

    try:
        db.session.delete(student)
        db.session.commit()
        flash(f'学生 {student_name} 已成功删除', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"删除学生失败: {str(e)}")
        flash(f'删除失败: {str(e)}', 'danger')

    return redirect(url_for('index'))


@app.route('/batch_delete', methods=['POST'])
def batch_delete():
    """批量删除学生"""
    try:
        student_ids = request.form.getlist('student_ids')

        if not student_ids:
            flash('请选择要删除的学生', 'warning')
            return redirect(url_for('index'))

        # 转换为整数列表
        student_ids = [int(id) for id in student_ids if id.isdigit()]

        if not student_ids:
            flash('无效的学生ID', 'danger')
            return redirect(url_for('index'))

        # 批量删除
        delete_count = Student.query.filter(Student.id.in_(student_ids)).delete(
            synchronize_session=False
        )
        db.session.commit()

        flash(f'成功删除 {delete_count} 名学生', 'success')

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"批量删除失败: {str(e)}")
        flash(f'批量删除失败: {str(e)}', 'danger')

    return redirect(url_for('index'))


@app.route('/export')
def export_students():
    """导出学生数据到Excel"""
    try:
        # 获取所有学生
        students = Student.query.all()

        if not students:
            flash('没有数据可以导出', 'warning')
            return redirect(url_for('index'))

        # 准备数据 - 使用更简单直接的方法
        data = []
        for student in students:
            # 直接构建字典，确保键名正确
            row = {
                '学号': student.student_id,
                '姓名': student.name,
                '年龄': student.age,
                '性别': student.gender,
                '专业': student.major,
                'GPA': float(student.gpa) if student.gpa else 0.0,
                'GPA等级': student.get_gpa_level(),
                '邮箱': student.email,
                '电话': student.phone if student.phone else '',
                '地址': student.address if student.address else '',
                '入学日期': student.enrollment_date.strftime('%Y-%m-%d') if student.enrollment_date else '',
                '创建时间': student.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            data.append(row)

        # 创建DataFrame
        df = pd.DataFrame(data)

        # 调试：打印DataFrame信息
        print(f"导出数据行数: {len(df)}")
        print(f"列名: {df.columns.tolist()}")
        if not df.empty:
            print("第一行数据:", df.iloc[0].to_dict())

        # 创建Excel文件
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='学生信息', index=False)

            # 自动调整列宽
            worksheet = writer.sheets['学生信息']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        cell_value = str(cell.value) if cell.value is not None else ""
                        if len(cell_value) > max_length:
                            max_length = len(cell_value)
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        output.seek(0)

        # 生成文件名
        filename = f'students_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        app.logger.error(f"导出数据失败: {str(e)}")
        import traceback
        traceback.print_exc()  # 打印详细错误信息
        flash(f'导出失败: {str(e)}', 'danger')
        return redirect(url_for('index'))


@app.route('/api/students', methods=['GET'])
def get_students_api():
    """获取学生列表API（JSON格式）"""
    try:
        students = Student.query.all()
        return jsonify([student.to_dict() for student in students])
    except Exception as e:
        app.logger.error(f"API获取学生列表失败: {str(e)}")
        return jsonify({'error': '获取数据失败'}), 500


# ==================== 错误处理 ====================

@app.errorhandler(404)
def page_not_found(error):
    """404页面"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """500页面"""
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """通用异常处理"""
    app.logger.error(f"未处理的异常: {str(error)}")
    flash('系统发生错误，请联系管理员', 'danger')
    return redirect(url_for('index'))


# ==================== 启动应用 ====================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("学生信息管理系统")
    print("=" * 60)
    print(f"数据库路径: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"调试模式: {app.config['DEBUG']}")
    print("=" * 60)
    print("访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60 + "\n")

    # 启动应用
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000
    )