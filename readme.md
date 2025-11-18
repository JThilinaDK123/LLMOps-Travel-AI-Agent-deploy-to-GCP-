# Deploying a Multi Agent Travel Planner on GCP

## Tech Stack

- LLM Groq  
- Crew AI  
- Tavily Search API
- Google Artifact Registry
- Google Kubernetes Cluster  
- Circle CI    

---

## Project Setup

### 1. Build the Virtual Environment

Before writing any code, create a virtual environment.

Steps:

1. Create a new folder in your local machine.  
2. Open the terminal inside the folder and run the following commands:

```bash
python -m venv venv
source venv/bin/activate
```

3. Create a `.env` file inside the root directory and add the following credentials:

```
GROQ_API_KEY=<your_groq_api_key>
```

4. Create the following folder structure:

```
static/style.css           
templates/index.html
app/app.py              # Flask Backend code
app/crew_runner.py      # Crew AI agent and tasks     
setup.py            # Project setup and management script
```

5. Run the following command to install the project in editable mode:

```bash
pip install -e .
```

## Dockerization

To containerize the application:

1. Create a `Dockerfile` in the root directory.  
2. Create a `kubernetes-deployment.yaml` file for Kubernetes deployment.  

Example structure:

```
Dockerfile
kubernetes.yaml
```

## CI/CD Pipeline

1. Create a `config.yml` inside the .circleci folder.  

---

## GCP Environment Setup

### 1. Create a GKE Cluster

Use the following configuration:

- Cluster Name: ai-travel-agent
- Region: us-central1  
- Access using DNS: Yes  
- Review and Create 

---

### 2. Create a Artifact Registry (Repository)

Use the following configuration:

- Repo Name: llmops-repo
- Format: Docker
- Region: us-central1   
- Review and Create 

---


## Circle CI Setup

Set up a CircleCI account:

- Sign up using your Google account. After creating the account, connect it to GitHub to access the repositories.
- Connect project to CircleCI and set Environment variables. Open CircleCI and go to the projects section.
- Connect CircleCI to the GitHub account
- Authorize CircleCI to access your GitHub repositories and select the project repository (CircleCI will automatically detect the .circleci/config.yml file.)
- Then configure project settings:
- Add Environment Variables under Project Settings → Environment Variables:

```bash
GCLOUD_SERVICE_KEY — your Base64-encoded GCP key
GOOGLE_PROJECT_ID — your GCP project ID
GKE_CLUSTER — your GKE cluster name
GOOGLE_COMPUTE_REGION — your compute region
```

How to obtain the `Base64-encoded GCP key`

- Run below code as a 'git bash' command. Copy whole the output (the encoded key)

```bash
cat gcp-key.json | base64 -w 0
```

Trigger the CI/CD pipeline !!!!!

It will show an error ('llmops-secrets' are not avialble)

### Apply llmops-secrets to the kubernetes cluster

Use the following configuration:

- Navigate to Kubernetes dashboard -> Workloads
- Click the application name -> Kubectl -> get yaml
- Paste the below two codes

```bash
gcloud container clusters get-credentials llmops-project \
--region us-central1 \
--project mlops-thilina
```

```bash
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="YOUR_GROQ_KEY" \
  --from-literal=TAVILY_API_KEY="TAVILY_API_KEY"
```

---


Trigger the CI/CD pipeline Again !!!!
