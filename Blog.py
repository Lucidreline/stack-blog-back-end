from application import db, ma
from datetime import datetime


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
