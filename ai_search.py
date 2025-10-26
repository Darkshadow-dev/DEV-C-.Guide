from flask import Flask, request, jsonify
from firebase_admin import credentials, initialize_app, db
import firebase_admin

# --- CONFIG ---
FIREBASE_CRED = "serviceAccountKey.json"  # Path to your Firebase key
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
        title = post.get("title", "").strip()
        content = post.get("content", "").strip()
        if query in title.lower() or query in content.lower():
            results.append({
                "id": pid,
                "title": title,
                "snippet": content[:100] + ("..." if len(content) > 100 else "")
            })

    # sort by title match first
    results.sort(key=lambda x: query not in x["title"].lower())
    return jsonify({"results": results[:20]})  # limit to 20 results

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)
