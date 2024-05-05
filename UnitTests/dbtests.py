import pytest
import sqlite3

@pytest.fixture
def db_connection():
    """Create a memory-based SQLite database connection."""
    connection = sqlite3.connect(':memory:')
    yield connection
    connection.close()

def setup_database(db_connection):
    """Create a table in the testing database."""
    cursor = db_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_data (
            id INTEGER PRIMARY KEY,
            info TEXT NOT NULL
        );
    """)
    db_connection.commit()

def test_table_creation(db_connection):
    """Test if the table is created successfully."""
    setup_database(db_connection)
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_data';")
    assert cursor.fetchone() is not None, "Table should be created."

def test_data_insertion(db_connection):
    """Test if data is inserted and committed successfully."""
    setup_database(db_connection)
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO test_data (id, info) VALUES (?, ?)", (1, 'test_info'))
    db_connection.commit()
    cursor.execute("SELECT * FROM test_data WHERE id = 1;")
    result = cursor.fetchone()
    assert result is not None, "Data should be inserted."
    assert result == (1, 'test_info'), "Data should match the inserted values."

def test_verify_commit(db_connection, setup_database):
    """Ensure that data persists beyond the transaction scope."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM test_data")
    results = cursor.fetchall()
    assert len(results) > 0, "No data was committed to the database."

# This part allows the pytest runner to execute the tests.
if __name__ == "__main__":
    pytest.main()
