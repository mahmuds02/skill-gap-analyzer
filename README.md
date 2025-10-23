# 🎯 AI Career Skill Gap Mapper

An AI-powered web application that analyzes resumes against job descriptions to identify skill gaps and provide personalized career advice.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)

**🌐 Live Demo:** http://3.93.16.35:8080  
**📦 GitHub:** https://github.com/mahmuds02/skill-gap-analyzer

---

## 📖 Overview

The AI Career Skill Gap Mapper helps job seekers understand how well their resume matches specific job requirements using Google's Gemini AI.

**Created by:** Saim Mahmud  
**Course:** DSA 587 - AI Engineering (Fall 2025)  
**Institution:** SUNY Buffalo State University

### The Problem

Job seekers struggle to objectively assess how well their resumes match job requirements. Manual comparison is time-consuming, subjective, and often misses implicit skills.

### The Solution

- Automatically extracts required skills from job descriptions
- Analyzes resumes to identify present, partial, and missing skills
- Calculates quantified match percentages (e.g., 75% match)
- Generates personalized career development recommendations
- Tracks analysis history for progress monitoring

**Transform 15 minutes of manual work into 15 seconds of AI-powered analysis.**

---

## ✨ Features

- 🤖 **AI-Powered Analysis** - Uses Google Gemini 2.5 Flash for intelligent skill extraction
- 📊 **Match Percentage** - Quantified compatibility score (0-100%)
- 🎨 **Color-Coded Results** - Green (present), Yellow (partial), Red (missing)
- 💡 **Career Advice** - Personalized, actionable recommendations
- 📜 **Analysis History** - Track progress across multiple applications
- 📄 **Dual Input** - Upload PDF or paste text
- 🔒 **Privacy-First** - Resume text not permanently stored
- ⚡ **Fast** - Results in 15-20 seconds
- 📱 **Responsive** - Works on desktop and mobile

---

## 🛠️ Technology Stack

**Backend:**
- Python 3.12
- Flask 3.0
- SQLAlchemy (ORM)
- PyPDF2 (PDF extraction)

**AI Model:**
- Google Gemini 2.5 Flash API

**Database:**
- PostgreSQL 16
- Two-table normalized schema (3NF)

**Frontend:**
- HTML5, CSS3, JavaScript
- Modern dark theme UI

**Deployment:**
- AWS Lightsail (Ubuntu 22.04)
- Gunicorn WSGI server (3 workers)
- systemd process management

---

## 🏗️ Architecture

User Browser
↓
Flask Application (Port 8080)
├─→ Gemini AI API (Skill Extraction & Analysis)
└─→ PostgreSQL Database (Results Storage)

### Data Flow

1. User submits job description + resume
2. Flask sends job description to Gemini → extracts skills (5 sec)
3. Flask sends resume + skills to Gemini → classifies each skill (10 sec)
4. Flask requests career advice from Gemini → generates recommendations (3 sec)
5. Results saved to PostgreSQL with unique session ID
6. User sees match percentage, skill breakdown, and advice
