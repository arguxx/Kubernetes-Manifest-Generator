from src.core.generator import generate_manifest


if __name__ == "__main__":
    print("=== logic Kubernetes Deployment Generator ===")
    name = input("Application Name: ").strip()
    image = input("Image: ").strip()

    replicas = input("Replicas (optional): ").strip() or None
    namespace = input("Namespace (optional): ").strip() or None

    ports_input = input("Ports (optional): ").strip()
    ports = [p.strip() for p in ports_input.split(",") if p.strip()] if ports_input else None

    # yaml_output = generate_manifest(name, image, replicas, namespace, ports)

    output_file = generate_manifest(name, image, replicas, namespace, ports)
    print(f"\n✅ Manifest created at: {output_file}")