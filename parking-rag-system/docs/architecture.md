# Parking RAG Reservation System Architecture

## Overview

The system is an AI-powered parking reservation chatbot based on Retrieval-Augmented Generation (RAG).

The architecture combines:
- Vector database retrieval
- Large Language Models
- Reservation workflow management
- Guardrails and security
- Evaluation metrics
- Dynamic parking data

---

## Components

### 1. RAG Chatbot
Handles:
- User interaction
- Question answering
- Retrieval-based responses

Technologies:
- LangChain
- ChromaDB
- HuggingFace Embeddings

---

### 2. Vector Database
Stores static parking information.

Examples:
- Parking rules
- Pricing
- Location details
- Reservation policies

---

### 3. Dynamic Data Layer
Stores:
- Parking availability
- Updated slot information

Implemented using CSV-based structured storage.

---

### 4. Guardrails Layer
Provides:
- Prompt injection detection
- Sensitive information filtering
- Security policy enforcement

---

### 5. Evaluation System
Measures:
- Recall@K
- Precision@K
- Retrieval latency

---

### 6. Automated Testing
Implemented using pytest.

Tests include:
- Retrieval testing
- Guardrail testing
- Reservation workflow testing
- Availability testing