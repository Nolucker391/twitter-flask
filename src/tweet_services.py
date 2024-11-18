from models import Session, User
import models


def get_author_id():
    session = Session()
    user = session.query(User).first()

    if user:
        user_id = user.id
    else:
        user_id = None
    session.close()
    return user_id


class TweetService:
    def __init__(self, db: Session):
        self.db = Session()

    def get_tweet(self, tweet_id: int):
        return self.db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()

    def create_tweet(self, tweet_data: dict, author_id: int):
        content = tweet_data.get("content")
        if content is None:
            return {"message": "Tweet content is missing"}, 400
        db_tweet = models.Tweet(content=content, author_id=author_id)
        self.db.add(db_tweet)
        self.db.commit()
        self.db.refresh(db_tweet)
        return db_tweet.id

    def delete_tweet(self, tweet_id: int, author_id: int):
        tweet = self.db.query(models.Tweet).filter(
            models.Tweet.id == tweet_id,
            models.Tweet.author_id == author_id).first()
        if tweet:
            self.db.delete(tweet)
            self.db.commit()
            return {"message": "Tweet was deleted successfully!"}
        else:
            return {"message": "Tweet not found or you don't have permission to delete it."}

    def like_tweet(self, tweet_id: int, user_id: int):
        tweet = self.db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
        if tweet:
            user = self.db.query(models.User).filter(models.User.id == user_id).first()
            if user:
                tweet.liked_by_users.append(user)
                self.db.commit()
                return {"message": "Tweet liked successfully!"}
            else:
                return {"message": "User not found."}
        else:
            return {"message": "Tweet not found."}

    def unlike_tweet(self, tweet_id: int, user_id: int):
        tweet = self.db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
        if tweet:
            user = self.db.query(models.User).filter(models.User.id == user_id).first()
            if user:
                tweet.liked_by_users.remove(user)
                self.db.commit()
                return {"message": "Tweet unliked successfully!"}
            else:
                return {"message": "User not found."}
        else:
            return {"message": "Tweet not found."}

    def follow_user(self, user_id: int, follower_id: int):
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            follower = self.db.query(models.User).filter(models.User.id == follower_id).first()
            if follower:
                user.followers.append(follower)
                self.db.commit()
                return {"message": "User followed successfully!"}
            else:
                return {"message": "Follower not found."}
        else:
            return {"message": "User not found."}

    def unfollow_user(self, user_id: int, follower_id: int):
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            follower = self.db.query(models.User).filter(models.User.id == follower_id).first()
            if follower:
                user.followers.remove(follower)
                self.db.commit()
                return {"message": "User unfollowed successfully!"}
            else:
                return {"message": "Follower not found."}
        else:
            return {"message": "User not found."}

    def get_timeline(self, user_id: int):
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            timeline = []
            for following_user in user.following:
                for tweet in following_user.authored_tweets:
                    timeline.append({"author_id": tweet.author_id, "content": tweet.content})
            return timeline
        else:
            return {"message": "User not found."}

    def get_current_user_profile(self, user_id: int):
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            return {"name": user.name}
        else:
            return {"message": "User not found."}

    def get_user_profile(self, user_id: int, profile_id: int):
        user = self.db.query(models.User).filter(models.User.id == profile_id).first()
        if user:
            return {"name": user.name}
        else:
            return {"message": "User not found."}
