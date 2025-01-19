from flask import Flask, render_template, request, jsonify
from reviews_extractor import extract_reviews  # Ensure this is correctly imported

app = Flask(__name__)

# Home page route - renders the HTML form
@app.route('/')
def home():
    return render_template('index.html')

# API route - accepts a URL and returns extracted reviews
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    url = request.args.get('url')  # Get URL from query parameter
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        # Extract reviews using the extract_reviews function from reviews_extractor.py
        reviews = extract_reviews(url)
        return jsonify({
            "reviews_count": len(reviews),
            "reviews": reviews
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
