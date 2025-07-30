def validate_dockerfile(dockerfile_content):
    # TODO: Integrate hadolint/yamllint
    if "FROM" in dockerfile_content:
        return True, []
    return False, ["FROM statement missing"]

def validate_k8s_yaml(yaml_content):
    if "apiVersion" in yaml_content:
        return True, []
    return False, ["apiVersion missing"]
