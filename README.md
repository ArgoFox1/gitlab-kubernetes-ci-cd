# GitLab-Kubernetes Project Setup Guide
![kubectl-logo-medium](https://github.com/ArgoFox1/JenkinsOnKubernetes/assets/105239243/d9c775e7-df19-4856-8d26-4c47fb4bf7b1)
![indir](https://github.com/user-attachments/assets/c70c5878-b1c7-4b0b-9e40-1cf64cbbf97f)

## 1. Start Minikube & Check status of the minikube
Minikube starting and checking:
```
minikube start
minikube status
```

## 2. Create Agent Config File
Go to the project section in GitLab and create it:

```
.gitlab/agents/<agent-name>/config.yaml
```

## 3. Connect Cluster in the "Operate" Section
- Navigate to the "Operate" section and click on **Connect Cluster**.
- choose the agent name you created.
- You will be provided with a code. Open a new terminal tab (`Ctrl+T`), paste the code, and run it to download the agent.

## 4. Create `values.yaml`
Create a `values.yaml` file in the project directory similar to the example provided in the project.

## 5. Deploy GitLab Runner
Run the following Helm command to Deploy the GitLab Runner:

This code basicly creates deployment and deployment creates  pods for the runner:

```
helm install gitlab-runner --namespace gitlab-runner -f values.yaml gitlab/gitlab-runner --create-namespace
```

## 6. Configure GitLab Runner Tags
Go to **Settings -> CI/CD -> Runners** in GitLab. A runner will be automatically created. In the **Edit** section, add the following tags:

- `docker`
- `k8s`
- `kaniko`
- `dind`

## 7. Add Variables in `.gitlab-ci.yml`
create variables, add the following variables under **Settings -> CI/CD -> Variables**:

- `DOCKER_REGISTRY`
- `DOCKER_REGISTRY_USER`
- `DOCKER_REGISTRY_PASSWORD`

## 8. Monitor Pods and Jobs
- Use the following command to check the status of the pods:

```
kubectl get pods -w
```

- You can also monitor the jobs by navigating to `builds/jobs` in GitLab to view the jobs defined in `.gitlab-ci.yml`.

# 9. Job Status
## The first job should succeed
   ![chrome-capture-2024-10-11](https://github.com/user-attachments/assets/9d76b3f5-c1fb-43ee-9cb5-37676fd5970f) 
## The second job will have a similar output as shown below.
  ![chrome-capture-2024-10-11 (1)](https://github.com/user-attachments/assets/c9252101-205d-42ad-9cea-1ea6057ab947)

## 10. After the second job
- Run the following command to get the internal IP of your nodes:

```
kubectl get nodes -o wide
```

- Take the **internal IP** from the output and append the service's port to access the project in the following format:

```
<internal-ip>:<service-port>
```
