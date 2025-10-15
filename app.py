from flask import Flask, render_template, request
import yaml

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/healtz', methods=['GET'])
def healtz():
    return "OK", 200

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name')
    image = request.form.get('image')
    replicas = request.form.get('replicas')
    namespace = request.form.get('namespace')
    ports_input = request.form.get('ports')
    action = request.form.get('action') 

    ports = [p.strip() for p in ports_input.split(",") if p.strip()] if ports_input else None

    container_ports = [{"containerPort": int(p)} for p in ports] if ports else None

    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name},
        "spec": {
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [
                        {"name": name, "image": image}
                    ]
                }
            }
        }
    }

    if namespace:
        deployment["metadata"]["namespace"] = namespace
    if replicas:
        deployment["spec"]["replicas"] = int(replicas)
    if container_ports:
        deployment["spec"]["template"]["spec"]["containers"][0]["ports"] = container_ports

    yaml_output = yaml.dump(deployment, sort_keys=False)
    # return f"<pre>{yaml_output}</pre>"

    if action == "generate":
        return f"<h3>Generated YAML:</h3><pre>{yaml_output}</pre><br><a href='/'>Back</a>"
    elif action == "print":
        return f"<h3>Print View:</h3><pre>{yaml_output}</pre><script>window.print()</script><br><a href='/'>Back</a>"


if __name__ == "__main__":
    app.run(debug=True)
