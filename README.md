<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=32&duration=3000&pause=1000&color=00FF88&center=true&vCenter=true&width=500&lines=🔨+HAMMER;LOAD+GENERATOR+v2.0;TERMUX+EDITION" alt="Typing SVG" />
</p>

<p align="center">
  <strong><i>⚡ "Test your limits before they test you." ⚡</i></strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Termux-Android-00C853?style=for-the-badge&logo=android&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-FFD700?style=for-the-badge&logo=opensourceinitiative&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-555555?style=for-the-badge&logo=linux&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Built%20With-❤️-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Coded%20By-Fix0%20Dev-FF69B4?style=for-the-badge" />
</p>

---

## 📌 Overview

**HAMMER** is a high-performance HTTP/HTTPS load generator built for **Termux** (Android) and Linux environments. It delivers real-time feedback with a beautiful terminal UI, color-coded output, and detailed JSON reports.

**Perfect for:**
- 🧪 Stress testing your own servers
- 📊 Benchmarking API endpoints
- 🔥 Identifying performance bottlenecks
- 🛡️ Validating infrastructure limits

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🚀 **Async Engine** | Built with `asyncio` + `aiohttp` for maximum concurrency |
| 📊 **Live Progress Bar** | Gradient-colored real-time progress with request count, success rate, and response times |
| 📈 **Detailed Statistics** | Total requests, success/failure rates, avg/min/max response times, **95th percentile** |
| 📝 **JSON Reports** | Every request logged with status, timing, and errors |
| 🎨 **Beautiful UI** | Clean box layout with Fix0 Dev branding and terminal colors |
| 📱 **Termux Optimized** | Runs perfectly on Android with no root required |
| ⚡ **Lightweight** | Minimal dependencies — just Python 3.8+ and `aiohttp` |

---

## 📦 Complete Termux Installation

> **Copy and paste this entire block into Termux — ONE COMMAND INSTALL:**

```bash
#!/bin/bash
# HAMMER — Complete Termux Install

echo "🔨 Installing HAMMER on Termux..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Update packages
pkg update && pkg upgrade -y

# Install dependencies
pkg install python python-pip git nano -y

# Install aiohttp
pip install aiohttp

# Clone repository
git clone https://github.com/YOUR_USERNAME/hammer.git

# Navigate to directory
cd hammer

# Make executable
chmod +x hammer.py

# Verify installation
python hammer.py --help

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Installation complete!"
echo "🚀 Run: python hammer.py http://localhost:8080 -c 50 -d 10"
echo "🔧 Coded by Fix0 Dev — Terminal Aesthetics Division"´´´
