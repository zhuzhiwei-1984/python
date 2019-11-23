from flask import Flask, render_template

全_app = Flask(__name__)


@全_app.route('/')
def 视图_主页():
    return render_template('index.html')


@全_app.route('/user/<name>')
def 视图_相册(name):
    return render_template('user.html', name=name)

@全_app.errorhandler(404)
def 视图_404(e):
    
    return render_template('404.html'), 200

if __name__ == "__main__":
    全_app.run(debug=True, port=80)