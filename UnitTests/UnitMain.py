import pytest
import sys
sys.path.insert(1, 'E:\\Andromeda\\pythonProject2\\Modules')
#from scratch import helloworld
import scratch as sc

sc.helloworld()

import sqlite3

@pytest.fixture
def db_connection():
    """Create and return a database connection, which is then destroyed."""
    conn = sqlite3.connect(':memory:')  # Use an in-memory database for tests
    yield conn
    conn.close()

@pytest.fixture
def setup_database(db_connection):
    """Create a table in the testing database."""
    cursor = db_connection.cursor()
    cursor.execute("""
        CREATE TABLE test_data (
            id INTEGER PRIMARY KEY,
            info TEXT NOT NULL
        );
    """)
    db_connection.commit()

def test_insert_data(db_connection, setup_database):
    """Test inserting data into the database and committing the transaction."""
    cursor = db_connection.cursor()
    sql_insert_data = "INSERT INTO test_data (info) VALUES (?)"
    info_text = "Sample commit test"
    cursor.execute(sql_insert_data, (info_text,))
    db_connection.commit()

    # Verify insertion
    cursor.execute("SELECT * FROM test_data WHERE info=?", (info_text,))
    result = cursor.fetchone()
    assert result is not None, "Data was not inserted."
    assert result[1] == info_text, "Inserted data does not match."

def test_verify_commit(db_connection, setup_database):
    """Ensure that data persists beyond the transaction scope."""
    cursor = db_connection.cursor()
    # This test assumes test_insert_data has run and committed data successfully.
    cursor.execute("SELECT * FROM test_data")
    results = cursor.fetchall()
    assert len(results) > 0, "No data was committed to the database."

