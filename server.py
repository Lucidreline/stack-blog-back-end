from flask import Flask, jsonify, request
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


class Blog(db.Model):  # Create model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # you don't need to give Text a size
    body = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # a toString
    def __repr__(self):
        return '<Blog %r>' % self.title  # this will be shown when you print for debugging


class BlogSchema(ma.Schema):
    class Meta:
        # choose what you want to be returned. Sometimes you don't want to return everything like a password
        fields = ("id", "title", "body", "date_created")


@app.route('/blogs')  # returns all blogs
def show_blogs():
    blogsToReturn = Blog.query.all()  # grabs all blogs from database
    # turns blogs into dictionary (objects)
    blogs_schema = BlogSchema(many=True)
    # create a dictionary to return
    output = {"blogs": blogs_schema.dump(blogsToReturn)}
    return jsonify(output)  # turns dictionary to json for API


# returns a blog when you give it the blog id
@app.route('/blog/<int:blog_id>')
def show_blog(blog_id):
    blogToReturn = Blog.query.get_or_404(blog_id)
    blog_schema = BlogSchema()
    output = {"blog": blog_schema.dump(blogToReturn)}
    return jsonify(output)


@app.route('/blog/new', methods=['POST'])  # Creates a new blog
def create_blog():
    body = request.json  # data coming in (in a dictionary)

    # creates a new Blog using the json data
    newBlog = Blog(title=body['title'], body=body['body'])
    db.session.add(newBlog)  # gets the new blog ready to commit into the db
    db.session.commit()  # commits the new blog into the db

    blog_schema = BlogSchema()  # creates a schema for returning the blog

    # returns the blog that was just created
    output = {"New Blog Added: ": blog_schema.dump(newBlog)}

    return jsonify(output)
