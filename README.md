# OFDA Backend Challenge

This project is a solution to Belvo's technical challenge, focused on extracting financial data through a simulated API.

The goal is to build a robust, resilient, and maintainable service capable of:
- Dynamically creating clients and consents.
- Handling external API instability (504 errors).
- Temporarily storing data in cache.
- Normalizing the retrieved information and returning a clear, standardized response.

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
├── clients/                  # External API communication (/dynamic-client, /consent)
│   ├── dynamic_client.py
│   └── consents.py
├── extractors/               # Fetches account, balance, and transaction data
│   └── extractor.py
├── normalizers/              # Converts raw data into Pydantic objects
│   └── normalizer.py
├── schemas/                  # Pydantic models used for input and output
│   ├── request.py
│   └── response.py
├── core/                     # Shared utilities
│   ├── cache.py
│   └── retry_utils.py
```

---

## ⚙️ How to Run

1. **Install the dependencies:**

```bash
pip install -r requirements.txt
```

2. **Start the application:**

```bash
uvicorn app.api.api:app --reload
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

## 🧠 Implemented Strategies

### ✅ TTL Cache

- `dynamic_client` and `consent` tokens are stored using `cachetools.TTLCache`.
- This avoids unnecessary requests and improves performance.

### ✅ Automatic Retry with Exponential Backoff

- All unstable calls to the external API use the `tenacity` library.
- In case of failure (e.g., 504), the request is automatically retried with increasing wait time.

### ✅ Data Normalization

- The extracted data is converted into Pydantic objects with essential, formatted, and standardized fields.
- The final response includes control fields like `summary`, total number of transactions, accounts, processing time, etc.

### ✅ Modular and Maintainable Code

- Each component has a single responsibility.
- Layers for extraction, caching, normalization, business logic, and external communication are well separated.

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
          "description": "Transfer",
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

## 🤖 AI Support

During the development of this project, I used AI (ChatGPT) as a **technical assistant and decision reviewer**. The AI helped:

- Validate ideas on structure and separation of concerns
- Suggest best practices with libraries like `tenacity` and `cachetools`
- Identify improvements in readability and organization
- Support the creation of this README

> All code was implemented by me, with conscious decisions and adaptation to the challenge requirements.  
> AI was used as a reasoning partner, not as a code writer. 😉

---

## 📌 Final Considerations

- The project was developed with focus on clarity, maintainability, and resilience.
- Pydantic was essential for ensuring consistency in both input and output.
- Retry and cache make the system robust against external failures and idempotent whenever possible.
