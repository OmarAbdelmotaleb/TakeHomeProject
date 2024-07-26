from flask import Flask, jsonify, request
from json import loads
import pandas as pd

app = Flask(__name__)

# 1.1 Data Processing
# NOTE: We will be storing in memory

playlist = pd.read_json('playlist.json')
playlist['rating'] = 0

# 1.2 Backend API to serve this normalized data

@app.route("/")
def home_page():
    return "<p>Welcome to the backend.</p>"

# 1.2.1 [MUST HAVE] Front end should be able to request ALL the items in a normalized data set.
# NOTE: I used orient="index" to match the indices from the example normalized data.
@app.route("/api/data")
def get_data():

    page = request.args.get('page', type=int)
    # If page is not given in the parameters, let's just return the whole thing by index.
    if page is None:
        return jsonify(loads(playlist.to_json(orient="index"))), 200

    per_page = request.args.get('per_page', default=10, type=int)
    
    # Calculate total pages based on size of the json data
    # If it's an odd amount, increase total pages to account for leftover
    total_pages = len(playlist) // per_page
    if len(playlist) % per_page != 0:
        total_pages += 1
    
    # This may seem redundant, but parsing with loads() removes unnecessary quotation marks.
    # This will be repeated for the returns.
    if 1 <= page <= total_pages:
        start = (page - 1) * per_page
        end = start + per_page
        paginated_data = playlist.iloc[start:end]
        return jsonify({
            'data': loads(paginated_data.to_json(orient="index")),
            'total_pages': len(playlist) // per_page,
            'current_page': page
        }), 200
    else:
        return jsonify({"error": "Invalid page number"}), 404

# 1.2.2 [MUST HAVE] Given a title as input, return all the attributes of that song.
@app.route("/api/data/<title>")
def get_attr_by_title(title):

    result = playlist[playlist['title'].str.lower() == title.lower()]

    if result.empty:
        return jsonify({"error": "Song not found"}), 404
    
    parsed = loads(result.to_json(orient="records"))
    return jsonify(parsed), 200

@app.route('/api/data/<title>/<column>')
def get_data_by_title_and_column(title, column):
    # Filter based on title (case-insensitive)
    result = playlist[playlist['title'].str.lower() == title.lower()]

    if result.empty:
        return jsonify({"error": "Song not found"}), 404

    if column not in playlist.columns:
        return jsonify({"error": "Invalid column name"}), 400

    # Extract the specific column and convert to JSON, just values will suffice
    column_data = loads(result[[column]].to_json(orient="values"))
    return jsonify(column_data), 200

# 1.2.3 [NICE TO HAVE] User should be able to rate a song using star rating.
@app.route('/api/data/<title>/rating/<int:rating>')
def rate_song(title, rating):
    
    # Rating from 1 to 5
    if 1 <= rating <= 5:
        
        # Get the matching rows ( this is to handle loc() )
        matching_rows = playlist['title'].str.lower() == title.lower()

        if matching_rows.any():
            # Update the rating for the matching song
            playlist.loc[matching_rows, 'rating'] = rating
            return jsonify({"message": f"Rated '{title}' with {rating}"}), 200
        
        else:
            return jsonify({"error": "Song not found"}), 404
        
    else:
        return jsonify({"error": "Invalid rating (must be 1-5)"}), 400 
