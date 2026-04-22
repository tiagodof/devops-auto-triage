# 🤖 DevOps Auto Triage

> **AI-powered GitHub Issues triage tool** — automatically categorises issues, estimates complexity, and suggests the best developer to assign, using LLMs and GitHub Actions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-ready-2088FF.svg)](https://github.com/features/actions)

---

## 🎯 What is DevOps Auto Triage?

DevOps Auto Triage is an open-source tool that integrates directly into your GitHub repository via **GitHub Actions**. Every time a new issue is opened, the AI automatically:

1. **Classifies** the issue type (bug, feature, documentation, question, security)
2. **Estimates complexity** using story points (1, 2, 3, 5, 8, 13)
3. **Suggests the best assignee** based on commit history and expertise
4. **Adds labels** and posts a structured triage comment

This eliminates manual triage overhead and ensures issues are routed to the right developer from the moment they are created.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Auto Classification** | Categorises issues into bug, feature, docs, question, or security |
| **Complexity Estimation** | Assigns Fibonacci story points based on issue description |
| **Smart Assignment** | Analyses commit history to suggest the most relevant developer |
| **Label Automation** | Creates and applies labels automatically |
| **Triage Comments** | Posts a structured AI-generated triage summary on each issue |
| **Configurable** | Fully customisable via a simple YAML config file |

---

## 🏗️ Architecture

```
devops-auto-triage/
├── .github/
│   └── workflows/
│       └── triage.yml          # GitHub Actions workflow
├── triage/
│   ├── __init__.py
│   ├── classifier.py           # AI-powered issue classification
│   ├── estimator.py            # Story point estimation
│   ├── assignee_suggester.py   # Developer matching via commit history
│   ├── github_client.py        # GitHub API wrapper
│   └── comment_builder.py      # Triage comment formatter
├── config/
│   └── triage_config.yml       # Customisation settings
├── tests/
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Add the workflow to your repository

Copy `.github/workflows/triage.yml` into your target repository.

### 2. Set up the secret

In your repository settings, add a secret named `OPENAI_API_KEY` with your OpenAI API key.

### 3. Configure (optional)

Edit `config/triage_config.yml` to customise labels, story point scale, and team members.

### 4. Open an issue

The workflow triggers automatically on every new issue. Within seconds, the AI will post a triage comment.

---

## 📋 Example Triage Output

When a new issue is opened, the bot posts:

```
🤖 AI Triage Report

Category:    🐛 Bug
Complexity:  3 story points (Medium)
Suggested:   @tiagodof (matched: 8 related commits in /auth module)
Labels:      bug, medium-complexity, backend

Summary: This issue describes a login token expiry problem in the authentication
module. Based on the description and codebase history, this is a medium-complexity
bug likely related to the JWT refresh logic.
```

---

## 🔧 Configuration

```yaml
# config/triage_config.yml
ai_model: gpt-4o-mini
story_points: [1, 2, 3, 5, 8, 13]
labels:
  bug: "d73a4a"
  feature: "0075ca"
  documentation: "0052cc"
  question: "d876e3"
  security: "e4e669"
team:
  - github_username: tiagodof
    expertise: [python, fastapi, devops]
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'feat: add my feature'`
4. Push and open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
