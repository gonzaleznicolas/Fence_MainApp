import uuid
import requests
from datetime import datetime
from fence import db
from fence.userModel import User
from fence.eventModel import Event

microserviceURL = "http://microservice-env.eba-m8eyw6ia.us-west-2.elasticbeanstalk.com/"


# returns posts whose content or title have the search_string as a substring
def search(search_string):
	response = requests.get(f"{microserviceURL}/post/search/{search_string}")
	if response.status_code != 200:
		raise Exception("Microservice Unavailable.")
	posts = response.json()
	# load the username for each post in posts
	for post in posts:
		# turn date string to python datetime
		post['time'] = datetime.strptime(post['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
		# load username
		usr = User.query.filter_by(id=post['author_id']).first()
		post['author'] = usr.username if usr is not None else None

	return posts


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
	event = Event(event_name='comment_on_post',
				  post_id=post_id,
				  author_id=author_id,
				  content=content,
				  time=datetime.now())
	db.session.add(event)
	db.session.commit()


def newPost(title, content, author_id):
	print(f"time we are writing in is {datetime.now()}")
	# write new event to the event table
	event = Event(event_name='new_post', title=title, content=content, author_id=author_id, time=datetime.now())
	db.session.add(event)
	db.session.commit()


def getPost(post_id):
	response = requests.get(f"{microserviceURL}/post/get/{post_id}")
	post = response.json()
	# turn date string to python datetime
	post['time'] = datetime.strptime(post['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
	# load username
	usr = User.query.filter_by(id=post['author_id']).first()
	post['author'] = usr.username if usr is not None else None
	return post


def getMostRecentPosts(numberOfPosts):
	response = requests.get(f"{microserviceURL}/post/get/most_recent/{numberOfPosts}")
	if response.status_code != 200:
		raise Exception("Microservice Unavailable.")
	posts = response.json()
	# load the username for each post in posts
	for post in posts:
		# turn date string to python datetime
		post['time'] = datetime.strptime(post['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
		# load username
		usr = User.query.filter_by(id=post['author_id']).first()
		post['author'] = usr.username if usr is not None else None

	return posts


def getAllPosts():
	response = requests.get(f"{microserviceURL}/post/get/all")
	if response.status_code != 200:
		raise Exception("Microservice Unavailable.")
	posts = response.json()
	# load the username for each post in posts
	for post in posts:
		# turn date string to python datetime
		post['time'] = datetime.strptime(post['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
		# load username
		usr = User.query.filter_by(id=post['author_id']).first()
		post['author'] = usr.username if usr is not None else None

	return posts


def getCommentsForPost(post_id):
	response = requests.get(f"{microserviceURL}/comments/get/{post_id}")
	comments = response.json()

	# set author for 3 levels of nested comments
	for comment0 in comments:
		# turn date string to python datetime
		comment0['time'] = datetime.strptime(comment0['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
		usr = User.query.filter_by(id=comment0['author_id']).first()
		comment0['author'] = usr.username if usr is not None else None
		for comment1 in comment0["comments"]:
			# turn date string to python datetime
			comment1['time'] = datetime.strptime(comment1['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
			usr = User.query.filter_by(id=comment1['author_id']).first()
			comment1['author'] = usr.username if usr is not None else None
			for comment2 in comment1["comments"]:
				# turn date string to python datetime
				comment2['time'] = datetime.strptime(comment2['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
				usr = User.query.filter_by(id=comment2['author_id']).first()
				comment2['author'] = usr.username if usr is not None else None

	return comments

