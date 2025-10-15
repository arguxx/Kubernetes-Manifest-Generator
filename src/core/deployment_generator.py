
import yaml


def generate(data):
    name = data.get('name')
    image = data.get('image')
    replicas = data.get('replicas')
    namespace = data.get('namespace')
    ports_input = data.get('ports')
    action = data.get('action') 

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
        return yaml_output
    elif action == "print":
        return yaml_output

