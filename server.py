from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
# to stop it from giving us warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init database
db = SQLAlchemy(app)

# Create model


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # a toString
    def __repr__(self):
        return '<Blog %r>' % self.title


class BlogSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "body", "date_created")


@app.route('/blogs')
def show_blogs():
    blogsToReturn = Blog.query.all()
    blogs_schema = BlogSchema(many=True)
    output = {"blogs": blogs_schema.dump(blogsToReturn)}
    return jsonify(output)


@app.route('/blog/<int:blog_id>')
def show_blog(blog_id):
    blogToReturn = Blog.query.get(blog_id)
    blog_schema = BlogSchema()
    output = {"blog": blog_schema.dump(blogToReturn)}
    return jsonify(output)
