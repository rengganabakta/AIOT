from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# In-memory storage for received data
data_history = []

# Simple HTML template to display the data
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="5">
    <title>ESP32 Data Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background: #f4f4f4; }
    </style>
</head>
<body>
    <h1>ESP32 Data Dashboard</h1>
    <p>Received {{ data_history | length }} entries.</p>
    <table>
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Value 1</th>
                <th>Value 2</th>
                <th>Value 3</th>
            </tr>
        </thead>
        <tbody>
            {% for entry in data_history %}
            <tr>
                <td>{{ entry.timestamp }}</td>
                <td>{{ entry.value1 }}</td>
                <td>{{ entry.value2 }}</td>
                <td>{{ entry.value3 }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
'''

@app.route('/data', methods=['POST'])
def receive_data():
    """
    Endpoint for ESP32 to POST JSON data:
    {
        "value1": <float>,
        "value2": <float>,
        "value3": <float>
    }
    """
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400

    # Add timestamp and store
    entry = {
        "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        "value1": payload.get('value1'),
        "value2": payload.get('value2'),
        "value3": payload.get('value3')
    }
    data_history.insert(0, entry)

    return jsonify({"status": "success"}), 200

@app.route('/')
def index():
    """Render the dashboard with the latest data entries"""
    return render_template_string(HTML_TEMPLATE, data_history=data_history)

if __name__ == '__main__':
    # Run the app on all IPs, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
