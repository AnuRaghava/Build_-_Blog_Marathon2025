# Build_-_Blog_Marathon2025
Source code for the food safety agent 
# Prototype to Production - Food Safety Agent Starter Files

repository where you'll build a production-ready food safety ADK agent step by step.

## 🚀 What You'll Build

In this lab, you'll focus on critical deployment aspects:

1. *Create a Firestore native DB* - Storage of your images and text
2. *Integrate the Cloud Run Deployment with an ADK agent* - Connect your agent to the cloud run model
3. *Test with ADK Web interface* - Validate your conversational agent works correctly
4. *Perform load testing* - Observe how both Cloud Run instances auto-scale under load

## 📁 Starter Structure


accelerate-ai-lab3-starter/
|------- README.md                  # This file
|------- main.py
|------- Dcokerfile 
|------- food-safety-agent/ [Directory can be empty]
|------- Requirements.txt
|--------Templates/
             |-----index.html


## 🎯 Files to Complete

You'll need to implement the following files by following the instructions below:

*Food Safety Agent:*

- 🚧 Project_home/ - food-safety-agent - empty directory
- 🚧 Project_home/Requirements.txt - Required models
- 🚧 Project_home/main.py - FastAPI server with endpoints
- 🚧 Project_home/Dockerfile - Container configuration

*Templates:*
- 🚧 Templates/index.html - UI configuration

## 📚 Getting Started
Here, we need to create a cloud native Firestore Google Cloud database.
Google Cloud Run: To host the Python application (Serverless).
Vertex AI (Gemini X.x): The "Brain" to analyze hygiene, expiry dates, and food quality.
Cloud Firestore: To store inspection logs and compliance history.
Python (Flask): To build the API.

Detailed code is attached in the backend
## 🔗 Resources
- [Gemini 3 Pro - AI Assistent Tool] (https://aistudio.google.com/prompts/1FBiLY0TrXx_bFXeW-6qGIOj2m0XHzz03)
- [Complete Solution](https://github.com/amitkmaraj/accelerate-ai-lab3-complete)
- [Google ADK Documentation](https://cloud.google.com/agent-development-kit)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)

