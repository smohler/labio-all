from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

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

@app.route('/')
def swagger_ui():
    return render_template_string(swagger_ui_template)

if __name__ == '__main__':
    app.run(debug=True)

