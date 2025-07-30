from bot.services.validator import validate_dockerfile, validate_k8s_yaml

def test_validate_dockerfile_good():
    content = "FROM python:3.8\nCMD python app.py"
    valid, errors = validate_dockerfile(content)
    assert valid
    assert errors == []

def test_validate_dockerfile_bad():
    content = "CMD python app.py"
    valid, errors = validate_dockerfile(content)
    assert not valid
    assert any("FROM" in e for e in errors)

def test_validate_k8s_yaml_good():
    content = "apiVersion: apps/v1\nkind: Deployment\nmetadata: {}"
    valid, errors = validate_k8s_yaml(content)
    assert valid
    assert errors == []

def test_validate_k8s_yaml_bad():
    content = "kind: Deployment\nmetadata: {}"
    valid, errors = validate_k8s_yaml(content)
    assert not valid
    assert any("apiVersion" in e for e in errors)
