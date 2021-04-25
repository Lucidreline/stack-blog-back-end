from Blog import Blog, BlogSchema
from flask import jsonify, request
from server import db, app


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
    output = {"createdBlog": blog_schema.dump(newBlog)}

    return jsonify(output)


# Edits an exsisting blog
@app.route('/blog/<int:blog_id>/update', methods=['PUT'])
def update_blog(blog_id):
    body = request.json  # data coming in (in a dictionary)

    # finds the
    blog = Blog.query.get_or_404(blog_id)

    blog.title = body['title']  # updates the data with the data coming in
    blog.body = body['body']

    db.session.add(blog)
    db.session.commit()  # commits the new blog into the db

    blog_schema = BlogSchema()  # creates a schema for returning the blog

    # returns the blog that was just eddited
    output = {"updatedBlog": blog_schema.dump(blog)}

    return jsonify(output)

# Deletes a blog just from it's id
@app.route('/blog/<int:blog_id>/delete', methods=['DELETE'])
def delete_blog(blog_id):
    body = request.json

    blogToDelete = Blog.query.get_or_404(blog_id)

    db.session.delete(blogToDelete)
    db.session.commit()

    blog_schema = BlogSchema()

    output = {"deletedBlog": blog_schema.dump(blogToDelete)}

    return jsonify(output)