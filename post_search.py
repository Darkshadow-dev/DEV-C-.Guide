from flask import Flask, request, jsonify
from firebase_admin import credentials, initialize_app, db
import firebase_admin

# --- CONFIG ---
FIREBASE_CRED = "serviceAccountKey.json"  # Your Firebase key
FIREBASE_DB_URL = "https://dev-community-91d29-default-rtdb.europe-west1.firebasedatabase.app/"

# --- INIT FIREBASE ---
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED)
    initialize_app(cred, {'databaseURL': FIREBASE_DB_URL})

app = Flask(__name__)

@app.route("/search", methods=["POST"])
def search_posts():
    data = request.get_json() or {}
    query = data.get("query", "").strip().lower()
    if not query:
        return jsonify({"results": []})

    posts = db.reference("posts").get() or {}
    results = []

    for pid, post in posts.items():
        title = post.get("title", "")
        content = post.get("content", "")
        if query in title.lower() or query in content.lower():
            results.append({
                "id": pid,
                "title": title,
                "content": (content[:120] + "...") if len(content) > 120 else content
            })

    # Sort results by whether the title matches first
    results.sort(key=lambda x: query not in x["title"].lower())
    return jsonify({"results": results[:20]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)
