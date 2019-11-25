from flask import Flask, render_template
import os

全_app = Flask(__name__)


@全_app.route('/')
def 视图_主页():
    return render_template('主页.html')

@全_app.route('/关于我们')
def 视图_关于我们():
    return render_template('关于我们.html')

@全_app.route('/家庭相册')
def 视图_家庭相册():
    数据表 = list()
    print('123')
    for _,目录,文件 in os.walk('python/static/家庭相册/'):
        for 下标, i in enumerate(文件):
            if 下标%2:
                数据表.append({"路径":"家庭相册/"+i, "类别":["女主人","小主子"]})
            else:
                数据表.append({"路径":"家庭相册/"+i, "类别":["女主人","小朱子"]})

    # print(os.getcwd())
    return render_template('家庭相册.html', 数据表=数据表)

@全_app.route('/家庭影院')
def 视图_家庭影院():
    return render_template('家庭影院.html')

@全_app.route('/家庭书屋')
def 视图_家庭书屋():
    return render_template('家庭书屋.html')

@全_app.errorhandler(404)
def 视图_404(e):
    
    return render_template('404.html'), 200

if __name__ == "__main__":
    全_app.run(debug=True, host="0.0.0.0",port=80)