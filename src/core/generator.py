import yaml
from pathlib import Path

def generate_manifest(name, image, replicas=None, namespace=None, ports=None, output_dir="manifests"):
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
                        {
                            "name": name,
                            "image": image,
                        }
                    ]
                },
            },
        },
    }

    if namespace:
        deployment["metadata"]["namespace"] = namespace
    if replicas:
        deployment["spec"]["replicas"] = int(replicas)
    if container_ports:
        deployment["spec"]["template"]["spec"]["containers"][0]["ports"] = container_ports

    Path(output_dir).mkdir(exist_ok=True)
    output_file = Path(output_dir) / f"{name}-deployment.yaml"

    with open(output_file, "w") as f:
        yaml.dump(deployment, f, sort_keys=False)

    return output_file