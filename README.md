# OFDA Backend Challenge

This project is a solution for Belvo's technical challenge, focused on extracting financial data through a simulated Open Finance API.

The goal is to build a robust, resilient, and maintainable service capable of:
- Dynamically creating clients and consents.
- Handling instability in the external API (504 errors).
- Storing temporary data in cache.
- Normalizing extracted data and returning a clear, standardized response.

---

## 🚀 Technologies Used

- **Python 3.11+**
- **FastAPI**
- **Pydantic**
- **Requests**
- **Tenacity** – for automatic retry with exponential backoff.
- **Cachetools** – for in-memory storage with TTL.

---

## 📂 Project Structure

```
app/
├── api/                      # Routes and controllers (FastAPI)
│   └── api.py
├── services/                 # Business logic
│   └── extract_service.py
├── clients/                  # Communication with external API (/dynamic-client, /consent)
│   ├── dynamic_client.py
│   └── consents.py
├── extractors/               # Retrieves account, balance and transaction data
│   └── extractor.py
├── normalizers/              # Converts raw data into Pydantic objects
│   └── normalizer.py
├── schemas/                  # Pydantic models for input and output
│   ├── request.py
│   └── response.py
├── core/                     # Shared utilities
│   ├── cache.py
│   ├── retry_utils.py
│   └── error_handlers.py
```

---

## ⚙️ How to Run

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Run the application:**

```bash
uvicorn app.api.api:app --reload --port 8001
```

3. **Make a request to the extraction endpoint:**

```http
POST /extract-financial-data
Content-Type: application/json
```

```json
{
  "name": "My App",
  "organization_name": "My Organization",
  "organization_id": "123",
  "user_document_number": "00011122233"
}
```

---

## ⚠️ Error Handling Strategy

This API was designed with robustness and clarity in mind when interacting with external services. All errors returned from the Open Finance engine (Belvo test API) are interpreted and translated into meaningful and consistent HTTP responses for the client.

### 🔄 External API Error Mapping

| External Status | Description                                  | Returned Status | Notes |
|-----------------|----------------------------------------------|-----------------|-------|
| `400`           | Bad request (from integration)               | `502`           | Request was incorrectly built by our backend |
| `401`           | Unauthorized / invalid credentials           | `502`           | Treated as upstream auth failure |
| `422`           | Validation error                             | `422`           | Returned to client with helpful `detail` |
| `404`           | Not found (e.g., dynamic client or consent)  | `404`           | Returned as-is with controlled message |
| `500`           | Internal server error from Belvo             | `502`           | External service instability |
| `504`           | Timeout                                      | `504`           | Retry attempts exhausted, service unresponsive |

### ✅ FastAPI Exception Handlers

The application defines custom exception handlers for:

- `HTTPException` → Maps structured errors (400, 401, 404, 422, 502, etc.)
- `Timeout` → Captures timeouts from the external API
- `RequestValidationError` → Catches invalid payloads received by this API
- `Exception` (generic) → Fallback for unexpected errors

All handlers return structured responses with meaningful `message` and `detail` fields, improving observability and helping clients quickly understand and react to problems.

---

## 🧠 Key Design Decisions

### ✅ In-Memory Caching with TTL

- `dynamic_client` and `consent` tokens are cached using `cachetools.TTLCache`
- Avoids unnecessary requests and improves performance

### ✅ Automatic Retry with Exponential Backoff

- All unstable external API calls are wrapped with the `tenacity` library
- On failures (e.g., 504), requests are automatically retried with increasing wait times

### ✅ Data Normalization

- Extracted data is converted into structured Pydantic models with only the necessary fields
- The response includes metadata like number of accounts, total transactions, execution time, etc.

### ✅ Modular, Maintainable Code

- Each component has a single responsibility
- The codebase is organized by domain: extraction, caching, normalization, API, integration, etc.

---

## 🧪 Example Response

```json
{
  "user_document": "00011122233",
  "extraction_date": "2025-07-12T13:02:06.320Z",
  "accounts": [
    {
      "account_id": "abc123",
      "account_type": "checking",
      "balance": {
        "ammount": 1000.0,
        "currency": "BRL"
      },
      "transactions": [
        {
          "transaction_id": "tx1",
          "transaction_type": "deposit",
          "transaction_status": "completed",
          "ammount": 1000.0,
          "currency": "BRL",
          "direction": "in",
          "description": "Transferência",
          "date": "2025-07-11T13:00:00.000Z"
        }
      ]
    }
  ],
  "summary": {
    "total_accounts": 1,
    "total_transactions": 1,
    "processing_time_ms": 273,
    "errors": []
  }
}
```

---

## 🔐 Security and Encryption

Handling sensitive financial and personal data requires careful attention to security—even in a simulated environment. This project includes encryption mechanisms for improved safety and good engineering practice.

### ✅ What was implemented:

- **Symmetric encryption** (AES-128 via `Fernet`) for storing sensitive tokens and IDs in memory.
- **Environment-based secret management** using the variable `CRYPTOGRAPHY_KEY` to store the encryption key securely.
- **Avoiding logging of PII (personally identifiable information)** like user documents or authorization tokens.
- **TTL-based cache expiration** to limit the lifetime of sensitive data.

### 🔒 What is encrypted?

| Data                     | Storage       | Encrypted? |
|--------------------------|----------------|-------------|
| `dynamic_client_token`   | In-memory      | ✅ Yes       |
| `consent_token`          | In-memory      | ✅ Yes       |
| `consent_id`             | In-memory      | ✅ Yes       |
| `user_document_number`   | As key only    | ❌ No (used as cache key, not encrypted) |

### 💡 Why not encrypt cache keys?

The `Fernet` algorithm produces a different ciphertext every time for the same input, making it unsuitable for lookup keys. Thus, only values are encrypted—keys remain in plain text, but are not logged or exposed in responses.

---

## ⚠️ To enable encryption

1. Generate a key using:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

2. Set it in your environment:

```bash
export CRYPTOGRAPHY_KEY="your-generated-key"
```

Or include it in a `.env` file and load it via `python-dotenv`.

---

## 🤖 AI Assistance

During the development of this project, I used ChatGPT as a **technical assistant and reviewer**. It helped me:

- Validate structural and design decisions
- Suggest best practices with tools like `tenacity` and `cachetools`
- Improve code readability and modularity
- Write and organize this README

> All code was written by me. The AI was used as a reasoning partner, not an executor. 😉

---

## 📌 Final Thoughts

- The project was designed with clarity, maintainability and resilience in mind.
- Pydantic was used extensively to ensure consistency in data modeling.
- Retry and caching mechanisms improve robustness and minimize external instability.


---

✅ Challenge delivered with purpose, clean code, and a little help from a dog named Liara. 💜