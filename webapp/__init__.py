from flask import Flask,render_template
from webapp.models import db
from webapp.extensions import permission
from webapp.config import Config
from flask import g


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
@permission
def user_info():
    """用户信息"""
    return 'this is sercert'

@app.before_request
def setg():
    g.user = '1'


if __name__ == '__main__':
    app.run()
