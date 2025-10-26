import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dev-community-91d29-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('posts')
print("✅ Connected. Listening for posts...")

def print_posts():
    posts = ref.get()
    if posts:
        for p in posts.values():
            print(f"{p['username']}: {p['title']}")
    else:
        print("No posts yet.")

print_posts()
