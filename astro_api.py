# from flask import Flask, request, jsonify
# from calculate_gmt_time_position_2 import calculate_planet_positions  # Import your function

# app = Flask(__name__)

# @app.route('/get_planets', methods=['POST'])
# def get_planet_positions():
#     data = request.get_json()  # Get JSON input from request
#     year = data.get('year')
#     month = data.get('month')
#     day = data.get('day')
#     hour = data.get('hour')
#     timezone = data.get('timezone')

#     # Call your function to calculate positions
#     print("Input is -->",year, month, day, hour, timezone)
#     result = calculate_planet_positions(year, month, day, hour, timezone)
    
#     return jsonify(result)  # Return JSON response

# if __name__ == '__main__':
#     app.run(host='localhost', port=9000, debug=True)  # Run API on port 8000

# from flask import Flask, request, jsonify
# from calculate_gmt_time_position_2 import calculate_planet_positions  # Import function

# app = Flask(__name__)

# @app.route('/get_planets', methods=['POST'])
# def get_planet_positions():
#     data = request.get_json()  # Get JSON input from request
#     year = data.get('year')
#     month = data.get('month')
#     day = data.get('day')
#     hour = data.get('hour')
#     timezone = data.get('timezone')

#     # Call your function to calculate positions
#     result = calculate_planet_positions(year, month, day, hour, timezone)
    
#     return jsonify(result)  # Return JSON response

# if __name__ == '__main__':
#     from os import environ
#     app.run(host='0.0.0.0', port=int(environ.get("PORT", 10000)), debug=False)  # Use dynamic PORT

import json
from calculate_gmt_time_position_2 import calculate_planet_positions

# Define sample input
data = {
    "year": 2025,
    "month": 3,
    "day": 10,
    "hour": 12,
    "timezone": "Asia/Kolkata"
}

# Generate output from your function
result = calculate_planet_positions(**data)

# Create `docs/` directory if it doesn't exist
import os
os.makedirs("docs", exist_ok=True)

# Save the output as `api.json`
with open("docs/api.json", "w") as f:
    json.dump(result, f, indent=4)

print("✅ API JSON Generated: docs/api.json")