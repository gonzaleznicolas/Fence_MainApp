import uuid
import requests
from datetime import datetime
from fence import db
from fence.userModel import User
from fence.eventModel import Event

microserviceURL = "http://microservice-env.eba-m8eyw6ia.us-west-2.elasticbeanstalk.com/"


def commentOnComment(post_id, parent_comment_id, author_id, content):
	event = Event(event_name='comment_on_comment',
				  post_id=post_id,
				  parent_comment_id=parent_comment_id,
				  author_id=author_id,
				  content=content,
				  time=datetime.now())
	db.session.add(event)
	db.session.commit()


def commentOnPost(post_id, author_id, content):
	comment_id = uuid.uuid1().int
	time = datetime.now()

	new_comment = {
		"comment_id": comment_id,
		"author_id": author_id,
		"time": time,
		"content": content,
		"comments": []
	}

	event = Event(event_name='comment_on_post',
				  post_id=post_id,
				  author_id=author_id,
				  content=content,
				  time=time)
	db.session.add(event)
	db.session.commit()


def newPost(title, content, author_id):
	post_id = uuid.uuid1().int
	time = datetime.now()

	# write new event to the event table
	event = Event(event_name='new_post', title=title, content=content, author_id=author_id, time=time)
	db.session.add(event)
	db.session.commit()


def getPost(post_id):
	response = requests.get(f"{microserviceURL}/post/get/{post_id}")
	post = response.json()

	# load username
	usr = User.query.filter_by(id=post['author_id']).first()
	post['author'] = usr.username if usr is not None else None
	return post


def getMostRecentPosts(numberOfPosts):
	response = requests.get(f"{microserviceURL}/post/get/most_recent/{numberOfPosts}")
	posts = response.json()
	# load the username for each post in posts
	for post in posts:
		# load username
		usr = User.query.filter_by(id=post['author_id']).first()
		post['author'] = usr.username if usr is not None else None

	return posts


def getAllPosts():
	response = requests.get(f"{microserviceURL}/post/get/all")
	posts = response.json()
	# load the username for each post in posts
	for post in posts:
		# load username
		usr = User.query.filter_by(id=post['author_id']).first()
		post['author'] = usr.username if usr is not None else None

	return posts


def getCommentsForPost(post_id):
	response = requests.get(f"{microserviceURL}/comments/get/{post_id}")
	comments = response.json()

	# set author for 3 levels of nested comments
	for comment0 in comments:
		usr = User.query.filter_by(id=comment0['author_id']).first()
		comment0['author'] = usr.username if usr is not None else None
		for comment1 in comment0["comments"]:
			usr = User.query.filter_by(id=comment1['author_id']).first()
			comment1['author'] = usr.username if usr is not None else None
			for comment2 in comment1["comments"]:
				usr = User.query.filter_by(id=comment2['author_id']).first()
				comment2['author'] = usr.username if usr is not None else None

	return comments

