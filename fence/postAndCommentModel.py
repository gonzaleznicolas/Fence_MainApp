from fence import db
from fence.userModel import User

posts = [
    {
        "id": "0",
        "author": "Joe Jackson",
        "title": "What is software?",
        "content": "Soeone explain it to me...",
        "comments": [
            {"id": "1", "level": 0, "user": "Jack", "content": "Ah"},
            {"id": "2", "level": 1, "user": "Charlie", "content": "What"},
            {"id": "3", "level": 2, "user": "Alice", "content": "Ok"},
            {"id": "4", "level": 2, "user": "Bob", "content": "lol"}
        ]
    },
    {
        "id": "1",
        "author": "Steve Terry",
        "title": "What is fence",
        "content": "What is this website?",
        "comments": []
    },
    {
        "id": "2",
        "author": "Mike Lund",
        "title": "I like software",
        "content": "Do you all agree?",
        "comments": [
            {"id": "1", "level": 0, "user": "Jared", "content": "love it!"},
            {"id": "3", "level": 1, "user": "keemstar", "content": "love you!"},
            {"id": "2", "level": 0, "user": "Jared", "content": "love it XD!"}
        ]
    }
]


