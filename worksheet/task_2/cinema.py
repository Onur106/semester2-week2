"""
This is where you should write your code and this is what you need to upload to Gradescope for autograding.

You must NOT change the function definitions (names, arguments).

You can run the functions you define in this file by using test.py (python test.py)
Please do not add any additional code underneath these functions.
"""

import sqlite3


def customer_tickets(conn, customer_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT f.title, s.screen, t.price
        FROM tickets t
        JOIN screenings s ON s.screening_id = t.screening_id
        JOIN films f ON f.film_id = s.film_id
        WHERE t.customer_id = ?
        ORDER BY f.title ASC
    """, (customer_id,))
    return cur.fetchall()


def screening_sales(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT s.screening_id, f.title, COUNT(t.ticket_id) AS tickets_sold
        FROM screenings s
        JOIN films f ON f.film_id = s.film_id
        LEFT JOIN tickets t ON t.screening_id = s.screening_id
        GROUP BY s.screening_id, f.title
        ORDER BY tickets_sold DESC
    """)
    return cur.fetchall()


def top_customers_by_spend(conn, limit):
    cur = conn.cursor()
    cur.execute("""
        SELECT c.customer_name, SUM(t.price) AS total_spent
        FROM customers c
        JOIN tickets t ON t.customer_id = c.customer_id
        GROUP BY c.customer_id, c.customer_name
        ORDER BY total_spent DESC
        LIMIT ?
    """, (limit,))
    return cur.fetchall()