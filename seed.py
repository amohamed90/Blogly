from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Add test users
user1 = User(first_name='Rocky', last_name="Dog")
user2 = User(first_name='Spike', last_name="Dog", image_url="https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500")
user3 = User(first_name='Socrates', last_name="Cat", image_url="https://previews.123rf.com/images/racorn/racorn1308/racorn130805649/21341221-profile-portrait-of-a-charming-young-business-woman-being-happy-and-smiling-in-an-office-setting-.jpg")

# Add test users
post1a = Post(title='Post1a', content="This is a post!", user_id=1)
post1b = Post(title='Post1b', content="This is a post2!", user_id=1)
post2a = Post(title='Post2a', content="This is a post3!", user_id=2)
post3a = Post(title='Post3a', content="This is a post4!", user_id=3)

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(post1a)
db.session.add(post1b)
db.session.add(post2a)
db.session.add(post3a)

# Commit--otherwise, this never gets saved!
db.session.commit()
