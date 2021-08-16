from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)



class News(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(255))
	context = db.Column(db.Text())
	imag = db.Column(db.Text())
	url = db.Column(db.String(255))

	def __init__(self, title, context, imag, url):
		self.title = title
		self.context = context
		self.imag = imag
		self.url = url
	def __repr__(self):
		return '<News %r>' % self.title

@app.route('/',methods=['GET'], defaults={"page": 1})
@app.route('/<int:page>', methods=['GET'])
def index(page):
	# page = page
	per_page = 10

	page = request.args.get('page', 1, type=int)
	news = News.query.order_by(News.id.desc()).paginate(page,per_page,error_out=False)
	next_url = url_for('index', page=news.next_num)
	prev_url = url_for('index', page=news.prev_num)

	return render_template('index.html', news=news.items, next_url=next_url, prev_url=prev_url)

if __name__ == '__main__':
   app.run(debug = True)