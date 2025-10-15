
import yaml


def generate(data):
    name = data.get('name')
    image = data.get('image')
    replicas = data.get('replicas')
    namespace = data.get('namespace')
    ports_input = data.get('ports')
    action = data.get('action') 

    if isinstance(ports_input, str):
        ports = [p.strip() for p in ports_input.split(",") if p.strip()]
    elif isinstance(ports_input, list):
        ports = [str(p).strip() for p in ports_input if str(p).strip()]
    else:
        ports = None

    try:
        container_ports = [{"containerPort": int(p)} for p in ports] if ports else None
    except ValueError:
        raise ValueError("Ports must be valid integers.")

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
        return yaml_output
    elif action == "print":
        return yaml_output

