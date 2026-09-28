from flask import Flask, request, jsonify, send_file
import AO3
import re
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/api/fetch')
def fetch_fic():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        match = re.search(r'works/(\d+)', url)
        if not match:
            return jsonify({"error": "INVALID_LINK"}), 400
        
        work_id = int(match.group(1))
        print(f"Attempting to fetch Work ID: {work_id}...")
        
        # Load the work using the ao3-api package
        work = AO3.Work(work_id)
        
        authors = ", ".join([a.username for a in work.authors]) if work.authors else "Anonymous"
        
        print(f"Success! Found: {work.title}")
        return jsonify({
            "title": work.title,
            "author": authors,
            "words": work.words,
            "url": url
        })
        
    except Exception as e:
        # This prints the EXACT error to your terminal so we can see what broke
        print("\n--- AO3 FETCH ERROR ---")
        print(f"Failed to fetch: {url}")
        traceback.print_exc()
        print("-----------------------\n")
        
        error_msg = str(e).lower()
        if "restricted" in error_msg or "login" in error_msg or "auth" in error_msg:
            return jsonify({"error": "LOCKED_FIC"}), 403
            
        # Send the actual error message back to the browser console
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Cozy AO3 Server at http://localhost:8000")
    app.run(port=8000, debug=True)