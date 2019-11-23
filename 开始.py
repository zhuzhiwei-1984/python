from flask import Flask, render_template

全_app = Flask(__name__)


@全_app.route('/')
def 视图_主页():
    return render_template('主页.html')

@全_app.route('/关于我们')
def 视图_关于我们():
    return render_template('关于我们.html')

@全_app.route('/家庭相册')
def 视图_家庭相册():
    return render_template('家庭相册.html')

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
    全_app.run(debug=True, port=80)