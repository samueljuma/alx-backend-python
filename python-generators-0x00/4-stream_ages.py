#!/usr/bin/env python3
"""
4-stream_ages.py
Stream user ages using a generator and compute memory-efficient average.
"""

seed = __import__('seed') # use connect_to_prodev from  seed.py


def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    Uses a single loop (for row in cursor).
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    try:
        for row in cursor:  # ✅ LOOP 1
            yield row[0]    # row = (age,), so yield the age value
    finally:
        cursor.close()
        connection.close()


def compute_average_age():
    """
    Uses the stream_user_ages generator to compute average age.
    Uses one loop only (for age in generator).
    """
    total = 0
    count = 0
    for age in stream_user_ages():  # ✅ LOOP 2
        total += age
        count += 1

    if count > 0:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")
    else:
        print("No users found.")
        
if __name__ == "__main__":
    compute_average_age()
