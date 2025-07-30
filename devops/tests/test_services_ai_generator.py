from bot.services.ai_generator import generate_docker_k8s

def test_generate_docker_k8s_stub():
    dockerfile, k8s_yaml = generate_docker_k8s("Python FastAPI app")
    assert isinstance(dockerfile, str)
    assert isinstance(k8s_yaml, str)
    assert "FROM" in dockerfile  # Because your stub includes FROM
    assert "apiVersion" in k8s_yaml  # Because your stub includes apiVersion
