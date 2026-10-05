# Agile Chatbot Application - Jenkins CI & Docker Sprint

This repository contains an **Agile Chatbot Application (`AgileBot`)** designed for an Agile Sprint focusing on **Continuous Integration (CI) with Jenkins and Docker**.

## 🚀 Repository Contents

- `src/chatbot.js`: Core Chatbot NLP Intent Matching engine.
- `src/server.js`: Express API server (`/api/chat` and `/api/health`).
- `public/`: Glassmorphism responsive Web Chat interface.
- `test/chatbot.test.js`: Automated unit test suite.
- `Dockerfile`: Multi-stage Docker build specification.
- `Jenkinsfile`: Declarative Jenkins CI Pipeline with 5 mandatory stages.
- `ASSIGNMENT_REPORT.md`: Full Sprint assignment documentation, logs, comparative analysis, and Agile CI/CD roadmap.

## 🛠️ Local Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Application Locally
```bash
npm start
# Open http://localhost:3000 in your browser
```

### 3. Run Automated Unit Tests
```bash
npm test
```

### 4. Build & Run Docker Container
```bash
docker build -t agile-chatbot-app:latest .
docker run -p 3000:3000 agile-chatbot-app:latest
```

## ⚙️ Jenkins CI Pipeline Stages

1. **Checkout**: Pulls latest commit from GitHub repository.
2. **Build**: Installs dependencies and runs syntax/lint checks.
3. **Test/Validate**: Executes unit test suite (`npm test`).
4. **Docker Build**: Packages app into tagged Docker container (`agile-chatbot-app:build-${BUILD_NUMBER}`).
5. **Result**: Validates container image and prints build telemetry.
