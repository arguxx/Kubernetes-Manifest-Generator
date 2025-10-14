import streamlit as st
from src.core.generator import create_deployment_yaml

st.set_page_config(page_title="Kubernetes Manifest Generator", page_icon="⚙️")

st.title("⚙️ Kubernetes Manifest Generator")
st.write("Generate Deployment manifest easily!")

app_name = st.text_input("App name", "myapp")
image_name = st.text_input("Docker image", "nginx:latest")
replicas = st.number_input("Replicas", min_value=1, value=2)

if st.button("Generate YAML"):
    output_file = create_deployment_yaml(app_name, image_name, replicas)
    st.success(f"✅ Manifest created: {output_file}")
    with open(output_file, "r") as f:
        st.code(f.read(), language="yaml")
