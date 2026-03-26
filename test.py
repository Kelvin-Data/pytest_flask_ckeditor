import pytest
from app import app
import sqlite3

@pytest.fixture
def client(tmp_path):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    test_db = tmp_path / "test_message.db"
    app.config['DATABASE'] = str(test_db)
    
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("""
        CREATE TABLE message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subscribe BOOLEAN,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    
def test_submit_form(client):
    response = client.post('/message', data={
        'name': 'Kelvin',
        'email': 'test@example.com',
        'subscribe': 'y',
        'message': 'Hello world'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"sent successfully" in response.data.lower()
    with app.test_client() as client:
        yield client

def test_db_insert(client):
    client.post('/message', data={
        'name': 'Kelvin',
        'email': 'test@example.com',
        'subscribe': 'y',
        'message': 'Hello world'
    }, follow_redirects=True)
    
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    c.execute("SELECT * FROM message")
    result = c.fetchall()
    conn.close()
    assert len(result) == 1
    row = result[0]
    assert row[1] == 'Kelvin'                
    assert row[2] == 'test@example.com'      
    assert row[3] == 1                       
    assert row[4] == 'Hello world'           
