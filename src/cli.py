from core.generator import create_deployment_yaml

def main():
    print("=== Kubernetes Manifest Generator ===")
    app_name = input("App name: ")
    image_name = input("Docker image: ")
    replicas = int(input("Replicas: "))

    output_file = create_deployment_yaml(app_name, image_name, replicas)
    print(f"\n✅ Manifest created at: {output_file}")

if __name__ == "__main__":
    main()
