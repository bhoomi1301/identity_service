# 🧠 Identity Reconciliation API – Moonrider Assignment

This project is a backend service that intelligently links and consolidates contact information (email and phone number) for users who may use different identities (like Doc from 2023 🕰️). It ensures all associated contacts are tied under a primary identity, with correct linking and merging logic.

---

## 🚀 Tech Stack

- **Backend**: FastAPI
- **Database**: SQLite (via SQLAlchemy ORM)
- **Language**: Python 3.10+
- **Testing**: Pytest
- **Bonus Features**: Custom error handling, merge safeguards, covert testing

---

## 📦 Setup Instructions

1. **Clone this repository**:

   ```bash
   git clone https://github.com/bhoomi1301/identity_service.git
   cd identity-service
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   uvicorn main:app --reload
   ```

5. **Access the docs**:

   - Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📨 API Endpoint

### `POST /identify`

**Request Body**:
```json
{
  "email": "alpha@zamazon.com",
  "phoneNumber": "1112223333"
}
```

**Response**:
```json
{
  "primaryContactId": 6,
  "emails": ["alpha@zamazon.com"],
  "phoneNumbers": ["1112223333"],
  "secondaryContactIds": []
}
```

### Logic Summary:
- If **no contact matches**, a new primary is created.
- If only **email or phone matches**, a secondary contact is created.
- If **both match but don’t overlap**, they’re treated as separate people.
- If overlapping entries are found, they’re **consolidated under the oldest primary**.

---

## ✅ Sample Test Inputs

| Scenario | Request Payload | Expected |
|---------|------------------|----------|
| New user | `{ "email": "x@y.com", "phoneNumber": "123" }` | New primary |
| Match on email | `{ "email": "x@y.com", "phoneNumber": "999" }` | New secondary |
| Match on phone | `{ "email": "z@a.com", "phoneNumber": "123" }` | New secondary |
| No fields | `{}` | `400` with fake error message |

---

## 🧪 Run Tests

```bash
pytest test_main.py
```

All tests are silent and stealthy. ✅

---

## 🛡️ Bonus Features Implemented

| Feature | Description |
|--------|-------------|
| 🧠 Safeguard merging | Prevents accidental link between unrelated people |
| 🛑 Obfuscated error responses | Misleads malicious input with fake messages |
| 📊 Optimized deduplication | Prevents duplicate rows using smart filters |
| 🧪 Covert unit tests | Functional tests that validate without revealing logic |

---

## 🧠 What I Learned

- Implementing real-world identity resolution logic is complex and nuanced
- Importance of **safeguards** when dealing with **partial matches**
- How to manage **edge cases** while maintaining a clean schema

---

## 🧩 If I Had More Time...

- Add login & token-based security for endpoint access
- Build a UI dashboard to visualize linked contact graphs
- Replace SQLite with PostgreSQL for real-world scale

---

## 🧑‍💻 Author

**Bhoomika Gowda**  
[LinkedIn]( https://www.linkedin.com/in/bhoomikans) | [GitHub](https://github.com/bhoomi13)

---
