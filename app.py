from flask import Flask, jsonify

app = Flask(__name__)

# Mock data for the sample endpoint
mock_data = {
    "sample123": {
        "labware": "test-labware",
        "volume": {
            "value": 10.5,
            "unit": "uL"
        },
        "conc": "test-conc"
    }
}

@app.route('/sample/<sampleID>', methods=['GET'])
def get_sample(sampleID):
    sample_data = mock_data.get(sampleID)
    if sample_data:
        return jsonify(sample_data), 200
    else:
        return jsonify({"error": "Sample not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
