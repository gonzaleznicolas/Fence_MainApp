import uuid
from datetime import datetime
from fence import db
from fence.userModel import User

fake_posts_db = { 
	12345: 
	{
		"id": 12345,
		"author_id": 1,
		"time": datetime.now(),
		"title": "This is a test title",
		"content": "What should I make the content of this post?"
	}
}

fake_comments_db = {
	12345: [
		{
			"comment_id": 111,
			"author_id": 1,
			"time": datetime.now(),
			"content": "What a stupid title...",
			"comments": [
				{
					"comment_id": 2222,
					"author_id": 2,
					"time": datetime.now(),
					"content": "I think its great",
					"comments": [
						{
							"comment_id": 444,
							"author_id": 1,
							"time": datetime.now(),
							"content": "Thank you :)",
							"comments": []
						},
					]
				},
				{
					"comment_id": 3333,
					"author_id": 3,
					"time": datetime.now(),
					"content": "Why do you guys care??",
					"comments": []
				},
			]
		}
	]
}

def commentOnPost(post_id, author_id, content):
	comment_id = uuid.uuid1().int
	time = datetime.now()

	comment = {
		"comment_id": comment_id,
		"author_id": author_id,
		"time": time,
		"content": content,
		"comments": []
	}

	fake_comments_db[post_id].append(comment)


# expected to store the post with the passed in title, content, and author_id
def newPost(title, content, author_id):
	post_id = uuid.uuid1().int
	time = datetime.now()

	# replace this with writing an event to the event database
	fake_posts_db[post_id] = {"id": post_id, "author_id": author_id, "time": time, "title": title, "content": content}


# input: integer (id of post to get)
# expected output: dictionary with the following format
# {
# 	"id": <int>
# 	"author_id": <int>
# 	"title": <string>
# 	"content": <string>
# }
def getPost(post_id):
	post = fake_posts_db[post_id] # replace this with getting post from microservice

	# load username
	post['author'] = User.query.filter_by(id=post['author_id']).first().username
	return post
	

# input: integer (number of posts to get)
# expected output: an array of post dictionaries, of at most size numberOfPosts
def getMostRecentPosts(numberOfPosts):
	posts = fake_posts_db # replace this with getting post from microservice

	# load the username for each post in posts
	for post_id in posts:
		post = posts[post_id]
		# load username
		post['author'] = User.query.filter_by(id=post['author_id']).first().username

	print(fake_posts_db)
	return posts.values()


# input: id of a post
# output: an array of comments in the following format:
def getCommentsForPost(post_id):
	comments = fake_comments_db.get(post_id, []) # replace this with a call to the microservice to get comments array

	# set author for 3 levels of nested comments
	for comment0 in comments:
		comment0["author"] = User.query.filter_by(id=comment0['author_id']).first().username
		for comment1 in comment0["comments"]:
			comment1["author"] = User.query.filter_by(id=comment1['author_id']).first().username
			for comment2 in comment1["comments"]:
				comment2["author"] = User.query.filter_by(id=comment2['author_id']).first().username

	return comments

