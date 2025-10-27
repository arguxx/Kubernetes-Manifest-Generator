import yaml
import sys,os
from pathlib import Path
import pytest

# import src.core.generator as gen
# import src.core.deployment_generator as dgen

from src.core import generator as gen
from src.core import deployment_generator as dgen


def test_generate_deployment_file_created(tmp_path):
    out = str(tmp_path)
    p = gen.generate_deployment(name="appx", image="nginx:1.2", replicas=2, ports=[8080], output_dir=out)
    assert p.exists()
    data = yaml.safe_load(p.read_text())
    assert data["metadata"]["name"] == "appx"
    assert data["spec"]["template"]["spec"]["containers"][0]["image"] == "nginx:1.2"
    assert data["spec"]["replicas"] == 2
    assert data["spec"]["template"]["spec"]["containers"][0]["ports"][0]["containerPort"] == 8080


def test_generate_deployment_no_ports(tmp_path):
    out = str(tmp_path)
    p = gen.generate_deployment(name="nop", image="busybox", output_dir=out)
    data = yaml.safe_load(p.read_text())
    # no ports key present
    assert "ports" not in data["spec"]["template"]["spec"]["containers"][0]


def test_deployment_generator_generate_yaml_contains_kind():
    data = {"name": "svc1", "image": "nginx", "replicas": 1, "ports": "80,443", "action": "generate"}
    out = dgen.generate(data)
    assert isinstance(out, str)
    assert "kind: Deployment" in out


def test_deployment_generator_ports_parsing_list():
    data = {"name": "svc2", "image": "nginx", "replicas": 1, "ports": [80, "443"], "action": "generate"}
    out = dgen.generate(data)
    assert "containerPort: 80" in out
    assert "containerPort: 443" in out


def test_generate_deployment_namespace_set(tmp_path):
    out = str(tmp_path)
    p = gen.generate_deployment(name="nsapp", image="nginx", namespace="myns", output_dir=out)
    data = yaml.safe_load(p.read_text())
    assert data["metadata"]["namespace"] == "myns"


# ---- failing tests (intentional) ----

def test_generate_deployment_wrong_apiVersion_fail(tmp_path):
    out = str(tmp_path)
    p = gen.generate_deployment(name="badapi", image="nginx", output_dir=out)
    data = yaml.safe_load(p.read_text())
    # intentionally wrong expectation to produce a failing test
    assert data["apiVersion"] == "v1"


def test_deployment_generator_invalid_ports_expect_no_exception():
    data = {"name": "svc3", "image": "nginx", "ports": "not-a-number", "action": "generate"}
    # this actually raises ValueError; the test expects no exception (so it will fail)
    _ = dgen.generate(data)


def test_generate_deployment_replicas_wrong_fail(tmp_path):
    out = str(tmp_path)
    p = gen.generate_deployment(name="rep", image="nginx", replicas=1, output_dir=out)
    data = yaml.safe_load(p.read_text())
    # incorrect expectation
    assert data["spec"]["replicas"] == 3


def test_deployment_generator_missing_image_fail():
    data = {"name": "svc4", "replicas": 1, "action": "generate"}
    out = dgen.generate(data)
    # expecting a specific image that won't be present
    assert "image: nginx" in out


def test_generate_deployment_ports_present_fail(tmp_path):
    out = str(tmp_path)
    p = gen.generate_deployment(name="noports", image="busybox", output_dir=out)
    data = yaml.safe_load(p.read_text())
    # expect ports but none provided
    assert "ports" in data["spec"]["template"]["spec"]["containers"][0]
