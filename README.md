# 👟 Personal Shopping Assistant

> **Le Wagon Data Science & AI Bootcamp — Batch #2201 (Online) — Graduation Project**

An AI-powered visual search and recommendation system for footwear, combining deep learning image classification, vector similarity search, and purchase behavior analysis.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-orange.svg)

---

## 🎯 Project Overview

**Problem:** Finding similar products in large e-commerce catalogs is challenging for users who know what they want visually but can't describe it in words.

**Solution:** Upload an image → Get visually similar products + frequently bought together recommendations, filtered by category and gender.

### Key Features
- 🔍 **Visual Search** — Find similar shoes using CLIP embeddings
- 🏷️ **Auto-Classification** — Automatic category & gender detection
- 🛒 **Sales-Based Suggestions** — "Frequently bought together" recommendations
- ⚡ **Real-time API** — Deployed on Google Cloud Run

---

## 📊 Dataset

**Source:** [H&M Personalized Fashion Recommendations](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations) (Kaggle)

| Component | Details |
|-----------|---------|
| Images | 5,156 shoe images (256×256 JPG) |
| Transactions | 738,255 purchase records |
| Categories | Boots, Sneakers, Sandals, Heels, Flat shoes, Slippers |
| Gender Groups | Baby/Children, Ladieswear, Menswear |

---

## 🧠 Models Architecture

### 1. CLIP Model (Visual Embeddings)

| Parameter | Value |
|-----------|-------|
| Architecture | ViT-B/32 (OpenAI pretrained) |
| Embedding Dimension | 512-D normalized vectors |
| Library | `open_clip` |
| Purpose | Visual similarity search |

### 2. Subcategory Classifier

| Parameter | Value |
|-----------|-------|
| Architecture | **EfficientNetB0** (transfer learning) |
| Classes | 6 (Boots, Sneakers, Sandals, Heels, Flat shoe, Slippers) |
| Test Accuracy | **83.2%** |

### 3. Gender Classifier

| Parameter | Value |
|-----------|-------|
| Architecture | **EfficientNetB1** (transfer learning) |
| Classes | 3 (Baby/Children, Ladieswear, Menswear) |
| Test Accuracy | **83.3%** |

---

## 🔄 Recommendation Pipeline

```
┌─────────────────┐
│   Input Image   │
└────────┬────────┘
         ▼
┌─────────────────────────────────────────┐
│  EfficientNetB0 → Subcategory           │
│  EfficientNetB1 → Gender                │
└────────┬────────────────────────────────┘
         ▼
┌─────────────────────────────────────────┐
│  CLIP ViT-B/32 → 512-D Embedding        │
└────────┬────────────────────────────────┘
         ▼
┌─────────────────────────────────────────┐
│  ChromaDB → Top-K Similar Items         │
│  (with optional category/gender filter) │
└────────┬────────────────────────────────┘
         ▼
┌─────────────────────────────────────────┐
│  Transaction Analysis → Co-purchases    │
└────────┬────────────────────────────────┘
         ▼
┌─────────────────────────────────────────┐
│  Combined Results                       │
│  (50% visual + 50% sales-based)         │
└─────────────────────────────────────────┘
```

---

## 🗄️ Vector Database (ChromaDB)

| Parameter | Value |
|-----------|-------|
| Storage | Persistent |
| Distance Metric | Cosine similarity |
| Items Stored | 5,156 embeddings + metadata |

---

## 🚀 API

**Endpoint:**
```
GET /predict?image_path=<URL>&top_k=6&subcategory=Auto&gender=Auto
```

**Response:** JSON array with product name, base64 image, price, category, gender

**Deployment:** Google Cloud Run

---

## 🎨 Frontend

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web application framework |
| **Custom CSS** | Styling & branding |
| **Font** | Roboto (Google Fonts) |

### UI Features
- Minimalist design with sharp edges
- Image URL input with category/gender filters
- Slider navigation for browsing recommendations
- Responsive two-column layout

---

## 📁 Project Structure

```
shopping-assistant/
├── api/                        # FastAPI backend
├── shoppingassistant/          # Core Python package
├── shopping-assistant-front/   # Streamlit frontend
│   ├── app.py
│   ├── styles.css
│   └── assets/
├── notebooks/                  # Training notebooks
├── raw_data/                   # H&M dataset
├── models/                     # Trained classifiers
├── Dockerfile
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **ML/DL** | TensorFlow, Keras, OpenCLIP, EfficientNet |
| **Vector DB** | ChromaDB |
| **Backend** | Python, FastAPI |
| **Frontend** | Streamlit, CSS |
| **Deployment** | Docker, Google Cloud Run |

---

## 🚀 Setup Instructions

### Frontend (this repo)

```bash
# Install dependencies
make install

# Run locally
make streamlit_local
```

### Requirements
- Python 3.9+
- See `requirements.txt` for dependencies

---

## 👥 Team

**Le Wagon Data Science & AI Bootcamp — Batch #2201 (Online)**

---

<p align="center">
  <b>🎓 Le Wagon Graduation Project 2025</b>
</p>
