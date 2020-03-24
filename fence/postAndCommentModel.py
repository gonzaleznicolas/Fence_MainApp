import uuid
from datetime import datetime
from fence import db
from fence.userModel import User

fake_posts_db = {}

fake_comments_db = {}

def newPost(title, content, author_id):
	post_id = uuid.uuid1().int
	time = datetime.now()

	# replace this with writing an event to the event database
	fake_posts_db[post_id] = {"id": post_id, "author_id": f"{author_id}", "title": title, "content": content}

def getPost(post_id):
	post = fake_posts_db[post_id] # replace this with getting post from microservice

	# load username
	post['author'] = User.query.filter_by(id=post['author_id']).first().username
	return post
	

def getCommentsForPost(post_id):
	return fake_comments_db[post_id]

def getMostRecentPosts(numberOfPosts):
	posts = fake_posts_db # replace this with getting post from microservice

	# load the username for each post in posts
	for post_id in posts:
		post = posts[post_id]
		# load username
		post['author'] = User.query.filter_by(id=post['author_id']).first().username

	print(fake_posts_db)
	return posts.values()

