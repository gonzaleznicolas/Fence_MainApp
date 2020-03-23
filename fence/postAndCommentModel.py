from datetime import datetime
from fence import db
from fence.userModel import User

posts = [
    {
        "id": "0",
        "author_id": "1",
        "title": "What is software?",
        "content": "Soeone explain it to me...",
    },
    {
        "id": "1",
        "author_id": "2",
        "title": "What is fence",
        "content": "What is this website?",
    },
    {
        "id": "2",
        "author_id": "3",
        "title": "I like software",
        "content": "Do you all agree?",
    }
]

comments = [
	[
		{"id": "1", "level": 0, "user": "Jack", "content": "Ah"},
		{"id": "2", "level": 1, "user": "Charlie", "content": "What"},
		{"id": "3", "level": 2, "user": "Alice", "content": "Ok"},
		{"id": "4", "level": 2, "user": "Bob", "content": "lol"}
	],
	[
		#empty
	],
	[
		{"id": "1", "level": 0, "user": "Jared", "content": "love it!"},
		{"id": "3", "level": 1, "user": "keemstar", "content": "love you!"},
		{"id": "2", "level": 0, "user": "Jared", "content": "love it XD!"}
    ]
]

def newPost(title, content, user_id):
	time = datetime.now()
	print('New post by %d at %s... %s: %s' % (user_id, time.strftime("%m/%d/%Y"), title, content))

def getPost(post_id):
	post = posts[post_id]
	post['author'] = User.query.filter_by(id=post['author_id']).first().username
	return post
	

def getCommentsForPost(post_id):
	return comments[post_id]

def getMostRecentPosts(numberOfPosts):
	return posts

