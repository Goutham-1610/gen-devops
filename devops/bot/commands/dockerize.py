from discord.ext import commands
import re
from services.github_client import fetch_repo_metadata
from services.ai_generator import generate_docker_k8s
from services.validator import validate_dockerfile, validate_k8s_yaml
import discord
import io

def is_github_url(text):
    return re.match(r"https?://github\.com/[\w\-]+/[\w\-]+", text.strip()) is not None

@commands.command(name="dockerize")
async def dockerize_cmd(ctx, *, input_text: str):
    await ctx.send("⏳ Working on your request...")
    repo_metadata = None

    if is_github_url(input_text):
        metadata = fetch_repo_metadata(input_text)
        repo_metadata = metadata
        await ctx.send(f"🔎 GitHub metadata found: {metadata}")
        prompt_input = f"GitHub repo: {input_text} ({metadata})"
    else:
        prompt_input = input_text

    dockerfile, k8s_yaml = generate_docker_k8s(prompt_input, repo_metadata=repo_metadata)

    # Validate Dockerfile
    docker_valid, docker_errors = validate_dockerfile(dockerfile)
    k8s_valid, k8s_errors = validate_k8s_yaml(k8s_yaml)

    if not docker_valid or not k8s_valid:
        errors = []
        if not docker_valid:
            errors.append(f"Dockerfile errors: {docker_errors}")
        if not k8s_valid:
            errors.append(f"Kubernetes YAML errors: {k8s_errors}")
        await ctx.send('\n'.join(errors))
        return
    # Send as attachments
    docker_bytes = dockerfile.encode("utf-8")
    k8s_bytes = k8s_yaml.encode("utf-8")
    await ctx.send(
        "✅ Done! Here are your generated files:",
        files=[
            discord.File(fp=io.BytesIO(docker_bytes), filename="Dockerfile"),
            discord.File(fp=io.BytesIO(k8s_bytes), filename="deployment.yaml")
        ]
    )

