import subprocess
import tempfile
import os
import shutil

def validate_dockerfile(dockerfile_content):
    hadolint_path = shutil.which("hadolint") or "/usr/local/bin/hadolint"
    if not os.path.isfile(hadolint_path):
        return False, ["Validation error (hadolint): hadolint not found"]

    with tempfile.NamedTemporaryFile("w+", suffix="Dockerfile", delete=False) as f:
        temp_path = f.name
        f.write(dockerfile_content)
    try:
        result = subprocess.run(
            [hadolint_path, temp_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, []
        else:
            return False, result.stdout.strip().splitlines()
    except Exception as e:
        return False, [f"Validation error (hadolint): {str(e)}"]
    finally:
        os.remove(temp_path)

def validate_k8s_yaml(yaml_content):
    kubeconform_path = shutil.which("kubeconform") or "/usr/local/bin/kubeconform"
    if not os.path.isfile(kubeconform_path):
        return False, ["Validation error (kubeconform): kubeconform not found"]

    with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as f:
        temp_path = f.name
        f.write(yaml_content)
    try:
        result = subprocess.run(
            [kubeconform_path, "-strict", "-summary", temp_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, []
        else:
            return False, result.stdout.strip().splitlines()
    except Exception as e:
        return False, [f"Validation error (kubeconform): {str(e)}"]
    finally:
        os.remove(temp_path)
