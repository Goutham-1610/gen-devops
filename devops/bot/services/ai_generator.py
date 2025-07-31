# bot/services/ai_generator.py
import google.generativeai as genai
import os
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_docker_k8s(input_text, repo_metadata=None):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are an expert DevOps engineer. Generate production-ready containerization files for:
    
    Input: {input_text}
    {f"Repository Info: {repo_metadata}" if repo_metadata else ""}
    
    Create:
    1. A secure, optimized Dockerfile with multi-stage builds if appropriate
    2. A complete Kubernetes deployment with service, configmap, and ingress if needed
    
    Format your response as:
    
    DOCKERFILE:
    ```
    [content]
    ```
    
    KUBERNETES:
    ```
    [content]
    ```
    """
    
    response = model.generate_content(prompt)
    content = response.text
    
    # Extract dockerfile and kubernetes sections
    dockerfile_match = re.search(r'DOCKERFILE:.*?``````', content, re.DOTALL)
    k8s_match = re.search(r'KUBERNETES:.*?``````', content, re.DOTALL)
    
    dockerfile = dockerfile_match.group(1).strip() if dockerfile_match else "FROM python:3.9-slim\nCOPY . .\nCMD python main.py"
    k8s_yaml = k8s_match.group(1).strip() if k8s_match else "apiVersion: apps/v1\nkind: Deployment"
    
    return dockerfile, k8s_yaml
