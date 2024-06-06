import praw
import config
import time
import os

def bot_login():
    print("Logging in...")
    r = praw.Reddit(username=config.username,
                    password=config.password,
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent=config.user_agent)
    return r

def run_bot(r, comments_replied_to):
    print("Obtaining 25 comments...")
    try:
        for comment in r.subreddit('aww').comments(limit=25):
            if "dog" in comment.body and comment.id not in comments_replied_to and not comment.author == r.user.me():
                print(f'String with "dog" found in comment {comment.id}')
                comment.reply("I love dogs! [Here](https://imgur.com/gallery/i-give-these-dogs-5-7-JGf6m) is an image of a dog.")
                print(f"Replied to comment {comment.id}")

                comments_replied_to.append(comment.id)

                with open("comments_replied_to.txt", "a") as f:
                    f.write(comment.id + "\n")

        # Sleep for 10 seconds
        time.sleep(10)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(10)

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
        # Create the file if it doesn't exist
        with open("comments_replied_to.txt", "w") as f:
            pass
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read().split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))  # Convert filter object to list

    return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)
while True:
    run_bot(r, comments_replied_to)
