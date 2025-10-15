from flask import Flask, render_template, request, jsonify, Response
from src.core.deployment_generator import generate as generate_deployment
import yaml

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/healtz', methods=['GET'])
def healtz():
    return "OK", 200

@app.route('/api/deployment/generate', methods=['POST'])
def generate():
    # data = json=request.form
    data = request.get_json()
    # return generate_deployment(data)
    respon = generate_deployment(data)
    return Response(respon, mimetype='text/plain')
    # return jsonify({"yaml": respon})

if __name__ == "__main__":
    app.run(debug=True)
