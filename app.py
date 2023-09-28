
from flask import Flask, render_template_string, send_from_directory, jsonify, request

app = Flask(__name__)

# Mock data for the sample endpoint
mock_data = {
    "sample123": {
        "labware": "test-labware",
        "volume": {
            "value": 10.5,
            "unit": "uL"
        },
        "conc": {
            "value": 5.0,
            "unit": "mg/ml"
        },
        "created": "2023-09-26T10:00:00Z"
    }
}

@app.route('/sample/<sampleID>', methods=['GET'])
def get_sample(sampleID):
    sample_data = mock_data.get(sampleID)
    if sample_data:
        return jsonify(sample_data)
    else:
        return jsonify({"error": "Sample not found"}), 404

@app.route('/sample/<sampleID>', methods=['POST'])
def update_sample(sampleID):
    if sampleID not in mock_data:
        return jsonify({"error": "Sample not found"}), 404

    data = request.json
    if 'volume' in data and 'value' in data['volume']:
        mock_data[sampleID]['volume']['value'] = data['volume']['value']
        return jsonify({"message": "Sample data updated successfully"})
    else:
        return jsonify({"error": "Bad request - invalid input"}), 400

@app.route('/')
def swagger_ui():
    return render_template_string(swagger_ui_template)

@app.route('/api/spec')
def api_spec():
    return send_from_directory('.', 'all_webapi_spec.yaml')

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
    app.run(debug=True)
