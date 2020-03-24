from datetime import datetime
from fence import db
from fence.userModel import User

test_posts = [
    {
        "id": "0",
        "author_id": "1",
        "title": "What is software?",
        "content": "Someone explain it to me...",
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

test_comments = [
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

def newPost(title, content, author_id):
	time = datetime.now()

	test_posts.append({"id": f"{len(test_posts)}", "author_id": f"{author_id}", "title": title, "content": content})

def getPost(post_id):
	post = test_posts[post_id] # replace this with getting post from microservice

	# load username
	post['author'] = User.query.filter_by(id=post['author_id']).first().username
	return post
	

def getCommentsForPost(post_id):
	return test_comments[post_id]

def getMostRecentPosts(numberOfPosts):
	posts = test_posts # replace this with getting post from microservice

	# load the username for each post in posts
	for post in posts:
		# load username
		post['author'] = User.query.filter_by(id=post['author_id']).first().username

	return posts

