
# Aadhaar OCR Extraction API

This project provides an **OCR-based Aadhaar Card information extractor** using **LangChain**, **OpenAI GPT-5**, and **FastAPI**.
It allows users to upload the **front and back images** of an Aadhaar card, and extracts structured information such as Aadhaar number, name, date of birth, gender, address, pincode, and issue date in **JSON format**.

---

## 📂 Project Structure

```
Adhaar/
│   .env                # Environment variables (API keys, configs)
│   main.py             # FastAPI entry point
│
├───OCR
│   │   aadhaar.py      # OCR extraction logic using LangChain + OpenAI
│   │   details.py      # Pydantic model for structured Aadhaar details
│   │   __init__.py
│   └───__pycache__w
│
└───__pycache__
```

---
## 🐳 Running with Docker

You can run this project easily using Docker without installing Python or dependencies.

### 1. Pull the image from Docker Hub
```bash
docker pull anuvratgautam/aadhaar-ocr:latest
```
---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd Adhaar
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate   # On Linux/Mac
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

Dependencies include:

* `fastapi`
* `uvicorn`
* `langchain`
* `langchain-openai`
* `pydantic`
* `python-dotenv`
* `python-multipart` (for file uploads)

4. **Set up environment variables**

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key
```

---

## ▶️ Running the Application

Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

The API will be available at:
👉 `http://127.0.0.1:8000`

Swagger UI (interactive API docs):
👉 `http://127.0.0.1:8000/docs`

---

## 📌 API Usage

### Endpoint: `/adhaar`

**Method:** `POST`
**Description:** Extract details from Aadhaar card front & back images.

#### Request (form-data):

* `phone` → Your phone number (integer)
* `front_image` → Aadhaar front image (JPG/PNG)
* `back_image` → Aadhaar back image (JPG/PNG)

#### Example (using `curl`):

```bash
curl -X POST "http://127.0.0.1:8000/adhaar" \
-F "phone=9876543210" \
-F "front_image=@1.jpg" \
-F "back_image=@2.jpg"
```

#### Response (JSON):

```json
{
  "aadhaar_number": "123456789012",
  "name": "Rahul Sharma",
  "father_husband_name": "Rajesh Sharma",
  "date_of_birth": "15/08/1995",
  "gender": "Male",
  "address": "123, MG Road, Delhi",
  "pincode": 110001,
  "issue_date": "20/01/2018",
  "phone_number": 9876543210
}
```

---

## 🏗 Code Overview

### 1. **`details.py`**

Defines the `Aadhaar_Details` Pydantic model for validating and structuring extracted Aadhaar data.

### 2. **`aadhaar.py`**

Contains the `AadhaarExtractor` class:

* Encodes Aadhaar images (front & back) in Base64
* Sends them to the OpenAI model with structured prompts
* Returns clean, structured JSON output

### 3. **`main.py`**

Exposes a FastAPI endpoint (`/adhaar`) that:

* Accepts Aadhaar images & phone number
* Calls `AadhaarExtractor.read_aadhaar()`
* Returns extracted JSON

---

## ⚠️ Notes & Limitations

* Requires **clear, readable Aadhaar images** for accurate extraction.
* Fields not visible will be returned as `"null"`.
* Aadhaar number must be exactly **12 digits**.
* **Do not share real Aadhaar numbers** when testing — use sample/demo Aadhaar cards.
