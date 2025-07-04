
## ✅ `seed.py` : What This Script Does

1. **Connects to MySQL** using the provided credentials.
2. **Creates a database** called `ALX_prodev` (if it doesn't exist).
3. **Creates a `user_data` table** with the following structure:
   - `user_id` (UUID, primary key)
   - `name` (string)
   - `email` (string)
   - `age` (decimal)
4. **Reads a CSV file (`user_data.csv`)** and inserts each row with a fresh UUID.
5. Provides a **generator** (`stream_users`) to stream rows from the table efficiently.

---

### Ensure MySQL Connector for Python is installed

```bash
pip install mysql-connector-python
```