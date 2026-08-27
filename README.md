# 🚀 DevOps CI/CD Project — Flask Application

> An end-to-end DevOps project demonstrating **GitHub → Jenkins → Docker → Docker Hub → Kubernetes (K3s)** with automated container deployment and rolling updates.


<img width="2208" height="1076" alt="image" src="https://github.com/user-attachments/assets/ca6d337c-e5e5-4cc5-bd63-b38b13c1412a" />



\

---

## 📌 Project Overview

This project demonstrates a complete CI/CD workflow for a simple Python Flask application.

Whenever a new version of the application is built, Jenkins:

1. Pulls the latest source code from GitHub.
2. Builds a Docker image.
3. Pushes the image to Docker Hub.
4. Deploys the new image to Kubernetes.
5. Performs a Kubernetes rolling update.
6. Verifies that the deployment completes successfully.

The application is then accessible through a Kubernetes **NodePort**.

---

## 🏗️ Architecture

```text
                     👩‍💻 Developer
                          │
                          │ git push
                          ▼
                     🐙 GitHub
                          │
                          │ Checkout
                          ▼
                     🔧 Jenkins
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
       🐳 Docker Build          Docker Push
              │                       │
              │                       ▼
              │                 🐳 Docker Hub
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
                  ☸️ Kubernetes / K3s
                          │
                     Deployment
                          │
                          ▼
                        Pod
                          │
                     Flask App
                          │
                          ▼
                  Kubernetes Service
                          │
                    NodePort :30080
                          │
                          ▼
                     🌐 Browser
```

---

## 🔄 CI/CD Pipeline

The Jenkins pipeline consists of the following stages:

```text
GitHub
   ↓
Checkout
   ↓
Docker Build
   ↓
Docker Push
   ↓
Kubernetes Deploy
   ↓
Rolling Update
   ↓
Success
```

### Pipeline stages

| Stage                 | Description                                          |
| --------------------- | ---------------------------------------------------- |
| **Checkout**          | Jenkins pulls the application from GitHub            |
| **Docker Build**      | Builds a Docker image using the Dockerfile           |
| **Docker Push**       | Pushes the versioned image to Docker Hub             |
| **Kubernetes Deploy** | Updates the Kubernetes Deployment with the new image |
| **Rolling Update**    | Kubernetes replaces the old Pod with the new version |
| **Success**           | Jenkins confirms the pipeline completed successfully |

---

## 🛠️ Technologies Used

* **Git** — Version control
* **GitHub** — Source code repository
* **Python 3.12** — Application runtime
* **Flask** — Web framework
* **Docker** — Application containerization
* **Docker Hub** — Container image registry
* **Jenkins** — CI/CD automation
* **Groovy** — Jenkins Pipeline
* **Kubernetes** — Container orchestration
* **K3s** — Lightweight Kubernetes distribution
* **AWS EC2** — Cloud infrastructure
* **PowerShell** — Local Windows environment
* **Linux / Amazon Linux** — Server environment

---

## 📂 Project Structure

```text
devops-app/
│
├── 📁 kubernetes/
│   ├── deployment.yaml
│   └── service.yaml
│
├── 📄 app.py
├── 🐳 Dockerfile
├── 📦 requirements.txt
├── 🚫 .gitignore
└── 📖 README.md
```

---

## 🐍 Application

The application is a simple Flask web application.

It listens on:

```text
Port: 5000
```

The application is configured to listen on all network interfaces:

```python
app.run(host="0.0.0.0", port=5000)
```

---

## 🐳 Docker

The Flask application is packaged into a Docker image.

Example image:

```text
reshu97/devops-app:12
```

Jenkins dynamically creates image tags based on the Jenkins build number.

For example:

```text
Build #10 → reshu97/devops-app:10
Build #11 → reshu97/devops-app:11
Build #12 → reshu97/devops-app:12
```

This provides a simple versioning mechanism for container images.

---

## ☸️ Kubernetes

The application is deployed to a Kubernetes cluster running on **K3s**.

### Deployment

The Kubernetes Deployment manages the application Pod.

Example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devops-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: devops-app
  template:
    metadata:
      labels:
        app: devops-app
    spec:
      containers:
        - name: devops-app
          image: reshu97/devops-app:1.0
          ports:
            - containerPort: 5000
```

The image is updated automatically by Jenkins during deployment.

---

## 🌐 Kubernetes Service

The application is exposed using a Kubernetes **NodePort** service.

```text
Application Port : 5000
NodePort         : 30080
```

Traffic flows as:

```text
Browser
   ↓
EC2 Public IP :30080
   ↓
Kubernetes NodePort
   ↓
Kubernetes Service :5000
   ↓
Flask Pod :5000
```

---

## 🔄 Rolling Updates

When Jenkins deploys a new image, Kubernetes performs a rolling update.

For example:

```text
Old Pod
devops-app-xxxxx
    │
    │
    ▼
New Pod created
devops-app-yyyyy
    │
    ▼
New Pod becomes Running
    │
    ▼
Old Pod terminates
```

This allows Kubernetes to replace the application version in a controlled way.

---

## 🔧 Jenkins Pipeline

The Jenkins pipeline performs the complete CI/CD workflow.

The deployment stage uses:

```groovy
stage('Kubernetes Deploy') {
    steps {
        sh '''
            export KUBECONFIG=/var/lib/jenkins/.kube/config

            kubectl set image deployment/devops-app \
            devops-app=reshu97/devops-app:${BUILD_NUMBER}

            kubectl rollout status deployment/devops-app
        '''
    }
}
```

The `${BUILD_NUMBER}` variable allows Jenkins to deploy the Docker image corresponding to the current Jenkins build.

For example:

```text
Jenkins Build #12
       ↓
Docker Image :12
       ↓
Docker Hub :12
       ↓
Kubernetes :12
```

---

## 🔐 Docker Hub Authentication

Jenkins authenticates with Docker Hub using a Jenkins credential:

```text
Credential ID:
dockerhub-creds
```

The Docker Hub credentials are stored in Jenkins rather than directly inside the Pipeline.

The pipeline uses:

```groovy
withCredentials([
    usernamePassword(
        credentialsId: 'dockerhub-creds',
        usernameVariable: 'DOCKER_USER',
        passwordVariable: 'DOCKER_PASSWORD'
    )
])
```

This keeps the credential out of the Jenkinsfile.

> ⚠️ Never commit Docker Hub passwords or Personal Access Tokens to GitHub.

---

## 🧪 Kubernetes Verification

The Kubernetes deployment is verified using:

```bash
kubectl rollout status deployment/devops-app
```

A successful deployment produces:

```text
deployment "devops-app" successfully rolled out
```

The running Pods can be checked using:

```bash
kubectl get pods
```

Example:

```text
NAME                          READY   STATUS    RESTARTS   AGE
devops-app-6c868b9497-f4rnl   1/1     Running   0          ...
```

The deployed image can be verified using:

```bash
kubectl get pod <POD_NAME> \
-o jsonpath='{.spec.containers[0].image}'
```

Example:

```text
reshu97/devops-app:12
```

---

## 🌐 Application Output

The application is exposed through the Kubernetes NodePort:

```text
http://<EC2-PUBLIC-IP>:30080
```

Example output:

```text
Hello from my DevOps project! 🚀 Running inside Docker!
```

After updating the application, the homepage displays the technologies demonstrated by this project.

---

## 📸 Screenshots

Screenshots can be stored inside:

```text
screenshots/
```

Recommended screenshots:

### Application

### Jenkins Pipeline

### Kubernetes

### Docker Hub

> Add these screenshots after creating the `screenshots` folder in the repository.

---

## 🚀 Deployment Workflow

### 1. Developer changes the application

Modify:

```text
app.py
```

### 2. Commit the changes

```bash
git add .
git commit -m "Update application"
```

### 3. Push to GitHub

```bash
git push
```

### 4. Jenkins retrieves the new code

Jenkins checks out the latest commit.

### 5. Jenkins builds the Docker image

```bash
docker build -t reshu97/devops-app:${BUILD_NUMBER} .
```

### 6. Jenkins pushes the image

```bash
docker push reshu97/devops-app:${BUILD_NUMBER}
```

### 7. Jenkins updates Kubernetes

```bash
kubectl set image deployment/devops-app \
devops-app=reshu97/devops-app:${BUILD_NUMBER}
```

### 8. Kubernetes performs a rolling update

```bash
kubectl rollout status deployment/devops-app
```

### 9. Application is updated

The new version becomes available through the Kubernetes NodePort.

---

## 📊 What This Project Demonstrates

### Source Control

* ✅ Git
* ✅ GitHub
* ✅ Git commits and branches
* ✅ GitHub repository management

### CI/CD

* ✅ Jenkins
* ✅ Jenkins Pipeline
* ✅ Groovy
* ✅ Automated Docker build
* ✅ Automated Docker push
* ✅ Automated Kubernetes deployment

### Containers

* ✅ Docker
* ✅ Dockerfile
* ✅ Docker image versioning
* ✅ Docker Hub
* ✅ Container registry authentication

### Kubernetes

* ✅ Kubernetes
* ✅ K3s
* ✅ Deployment
* ✅ Pods
* ✅ Services
* ✅ NodePort
* ✅ Rolling Updates
* ✅ `kubectl`
* ✅ Kubernetes configuration

### Cloud

* ✅ AWS EC2
* ✅ Security Groups
* ✅ Linux server administration

---

## 🎯 Project Outcome

This project demonstrates how a developer's code can move from source control to a running application through an automated DevOps pipeline:

```text
Developer
    ↓
GitHub
    ↓
Jenkins
    ↓
Docker
    ↓
Docker Hub
    ↓
Kubernetes / K3s
    ↓
AWS EC2
    ↓
Running Application
```

The project provides hands-on experience with **containerization, CI/CD automation, container registries, Kubernetes deployments, rolling updates, and cloud infrastructure**.

---

## 🔮 Future Improvements

Planned improvements for the project include:

* [ ] Add automated application tests
* [ ] Add SonarQube code quality analysis
* [ ] Add OWASP Dependency-Check
* [ ] Add Trivy container vulnerability scanning
* [ ] Add Kubernetes health probes
* [ ] Add resource limits and requests
* [ ] Add Kubernetes Secrets
* [ ] Add Jenkins GitHub webhook for automatic builds
* [ ] Add monitoring with Prometheus
* [ ] Add Grafana dashboards
* [ ] Add Terraform infrastructure provisioning
* [ ] Improve Kubernetes deployment strategy
* [ ] Add production-style logging

---

## 👩‍💻 Author

**Reshma**

This project was created as a hands-on DevOps learning project to understand the complete journey from source code to a containerized and Kubernetes-deployed application.

---

⭐ **If you found this project useful, feel free to explore the repository and follow the CI/CD workflow.**
