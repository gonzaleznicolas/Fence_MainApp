from fence import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    event_name = db.Column(db.String(45))
    title = db.Column(db.String(150))
    content = db.Column(db.String(3000))
    author_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    post_id = db.Column(db.Integer)
    parent_comment_id = db.Column(db.Integer)

    # this defines how to print a user. Useful for interacting with DB from command line
    def __repr__(self):
        return f"Event('{self.id}' ,'{self.event_name}' ,'{self.title}' ,'{self.content}' ,'{self.author_id}' ,'{self.time}' ,'{self.post_id}', '{self.parent_comment_id}')"

