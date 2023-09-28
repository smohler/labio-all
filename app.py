
from flask import Flask, render_template_string, send_from_directory, jsonify, request
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to generate a random sampleID with 8 characters (capital letters and digits)
def generate_sampleID():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def generate_sampleMaterial():
    return random.choice(["DNA", "PRO", "CEL", "BAC"])

def random_date(start, end):
    """Generate a random datetime between `start` and `end`."""
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# Function to generate the samples_db
def generate_samples_db(num_samples):
    samples = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)  # 5 years ago

    for _ in range(num_samples):
        sampleID = generate_sampleID()
        samples[sampleID] = {
            "material": generate_sampleMaterial(), 
            "labware": random.choice(
                            [
                                {"vendor":"epitube", "catalog":"0030123611"},
                                {"vendor":"azenta", "catalog":"68-1003-10"}
                            ]
                        ),
            "volume": {
                "value": round(random.uniform(500, 1400), 2),
                "unit": "uL"
            },
            "conc": {
                "value": round(random.uniform(1.0, 10.0), 2),
                "unit": "mg/ml"
            },
            "created": random_date(start_date, end_date).isoformat() + "Z"
        }
    return samples

# Generating the samples_db with 10,000 data points
samples_db = generate_samples_db(10000)

@app.route('/samples', methods=['GET'])
def get_all_sample_ids():
    return jsonify(list(samples_db.keys()))

@app.route('/sample/<sampleID>', methods=['GET'])
def get_sample(sampleID):
    sample_data = samples_db.get(sampleID)
    if sample_data:
        return jsonify(sample_data)
    else:
        return jsonify({"error": "Sample not found"}), 404

@app.route('/sample/<sampleID>', methods=['POST'])
def update_sample(sampleID):
    if sampleID not in samples_db:
        return jsonify({"error": "Sample not found"}), 404

    data = request.json
    if 'volume' in data and 'value' in data['volume']:
        samples_db[sampleID]['volume']['value'] = data['volume']['value']
        return jsonify({"message": "Sample data updated successfully"})
    else:
        return jsonify({"error": "Bad request - invalid input"}), 400

@app.route('/')
def swagger_ui():
    return render_template_string(swagger_ui_template)

@app.route('/api/spec')
def api_spec():
    return send_from_directory('.', 'swagger.yaml')

# Swagger UI template
swagger_ui_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Swagger UI</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css" >
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script>
    window.onload = function() {
        const ui = SwaggerUIBundle({
            url: "/api/spec",
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
            ],
            layout: "BaseLayout",
            deepLinking: true
        });
    }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
