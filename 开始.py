from flask import Flask, render_template, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField,FileField, SubmitField, BooleanField,SelectMultipleField, PasswordField
from wtforms.validators import DataRequired, AnyOf
from flask_wtf.file import FileField as File, FileRequired, FileAllowed
from bson import ObjectId
import os
import pymongo

全_app = Flask(__name__)
全_app.config['SECRET_KEY'] = '朱志伟爱常文斌'
全_数据库 = pymongo.MongoClient('192.168.31.220')
全_相册数据库游标 = 全_数据库['网站数据']['家庭相册']
全_账户数据库游标 = 全_数据库['网站数据']['账户信息']

class 类_相册提交表单(FlaskForm):
    '''相册提交表单类'''
    字符串 = StringField(label='请输入图像介绍', validators=[DataRequired('数据不能为空')])
    文件 = FileField(label='请选择上传的图片', validators=[FileRequired('数据不能为空'), FileAllowed(['jpg','jpeg','png','gif'])])
    类别 = SelectMultipleField(label='请选择类型',choices=[('小主子','小主子'), ('小朱子','小朱子'),('小兔子','小兔子'),('其他','其他')])
    提交按钮 = SubmitField('提交')

class 类_后台登录表单(FlaskForm):
    '''后台登录表单模块'''
    账户 = StringField(label='请输入用户名', validators=[DataRequired('用户名不能为空')])
    密码 = PasswordField(label='请输入密码', validators=[DataRequired('密码不能为空')])
    登录按钮 = SubmitField('提交')

@全_app.route('/')
def 视图_主页():
    return render_template('主页.html', 状态信息 = session.get('权限','假'))




@全_app.route('/关于我们')
def 视图_关于我们():
    return render_template('关于我们.html',状态信息 = session.get('权限','假'))

@全_app.route('/家庭相册')
def 视图_家庭相册():
    数据表 = list()
    数据表 = 全_相册数据库游标.find().sort("_id",-1)
    return render_template('家庭相册.html', 数据表=数据表,状态信息 = session.get('权限','假'))


@全_app.route('/删除相册/<fileID>')
def 视图_删除相册(fileID):
    print(fileID)
    
    路径 = 全_相册数据库游标.find_one({"_id":ObjectId(fileID)})
    # os.remove(os.path.join(os.getcwd(), 'python/static',路径['路径']))
    os.rename(os.path.join(os.getcwd(), 'python/static',路径['路径']) ,os.path.join(os.getcwd(), 'python/static/删除相册',路径['路径']))
    全_相册数据库游标.remove({"_id":ObjectId(fileID)})
    return redirect(url_for('视图_家庭相册'))

@全_app.route('/家庭影院')
def 视图_家庭影院():
    return render_template('家庭影院.html',状态信息 = session.get('权限','假'))

@全_app.route('/家庭书屋')
def 视图_家庭书屋():
    return render_template('家庭书屋.html',状态信息 = session.get('权限','假'))

@全_app.route('/后台登录', methods=['GET','POST'])
def 视图_后台登录():
    局_登录表单 = 类_后台登录表单()
    局_状态信息 = '请输入登录信息:'
    if 局_登录表单.validate_on_submit():
        局_账号 = 局_登录表单.账户.data
        局_密码 = 局_登录表单.密码.data
        局_数据核实 = 全_账户数据库游标.find_one({'账号':局_账号})
        if not 局_数据核实:
            局_状态信息 = '账号错误,请重新输入'
        elif 局_数据核实['密码'] != 局_密码:
            局_状态信息 = '密码错误,请重新输入'
        else:
            session['权限'] = '真'
            局_状态信息 = '登录成功!!'
            return render_template('后台登录.html', 提示信息=局_状态信息,状态信息 = session.get('权限','假'))
    return render_template('后台登录.html', 登录表单 = 局_登录表单, 提示信息=局_状态信息,状态信息 = session.get('权限','假'))

@全_app.route('/相册提交', methods=["GET", "POST"])
def 视图_相册提交():
    # 创建表单对象, 如果是post请求,前端发送了数据,flask会吧数据在构造的表单对象的时候,存放到对象中
    相册提交表单 = 类_相册提交表单()
    # 判断相册提交表单中的数据是否合理
    # 如果表单中的数据完全满足所有的验证器,则返回真
    if 相册提交表单.validate_on_submit():
        # 表示验证合格
        # 提取数据
        局_字符串 = 相册提交表单.字符串.data
        局_文件 = 相册提交表单.文件.data
        局_文件名 = 局_文件.filename
        局_文件.save('python/static/家庭相册/'+局_文件名)
        局_插入数据 = { '路径':'家庭相册/'+局_文件名,
                        '说明': 局_字符串,
                        '类别': 相册提交表单.类别.data
        }
        if not [文件 for 文件 in 全_相册数据库游标.find({'路径':'家庭相册/'+局_文件名})]:
            print('添加一条数据!')
            全_相册数据库游标.insert_one(局_插入数据)
            return render_template('相册提交.html', 表单 = 相册提交表单,状态信息 = session.get('权限','假'))
        else:
            print('发现重复数据')
            return render_template('相册提交.html', 表单 = 相册提交表单,状态信息 = session.get('权限','假'))

    return render_template('相册提交.html', 表单 = 相册提交表单,状态信息 = session.get('权限','假'))

@全_app.errorhandler(404)
def 视图_404(e):
    
    return render_template('404.html',状态信息 = session.get('权限','假')), 200

if __name__ == "__main__":
    全_app.run(debug=True, host="0.0.0.0",port=80)