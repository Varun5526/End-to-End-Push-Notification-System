from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for cross-origin requests

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            user='root',       
            password='varun5526',  
            database='instagram'  
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Serve Frontend
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Endpoint to store notification
@app.route('/store-notification', methods=['POST'])
def store_notification():
    data = request.json
    title = data.get('title')
    body = data.get('body')
    notification_type = data.get('type')  # Default to foreground
    source = data.get('source', 'Instagram')  # Default to Instagram

    if not title or not body:
        return jsonify({"error": "Title and body are required"}), 400

    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO notifications (title, body, type, source)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE received_at = CURRENT_TIMESTAMP
        """
        cursor.execute(query, (title, body, notification_type, source))
        connection.commit()
        return jsonify({"message": "Notification stored successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Endpoint to get notification count
@app.route('/notification-count', methods=['GET'])
def get_notification_count():
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM notifications")
        result = cursor.fetchone()
        total = result[0] if result else 0
        return jsonify({"total": total}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Endpoint to get recent notifications
@app.route('/recent-notifications', methods=['GET'])
def get_recent_notifications():
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        # Get last 10 notifications ordered by most recent
        cursor.execute("""
            SELECT id, title, body, type, source, received_at 
            FROM notifications 
            ORDER BY received_at DESC 
            LIMIT 10
        """)
        notifications = cursor.fetchall()
        
        # Convert datetime to string for JSON serialization
        for notif in notifications:
            if notif['received_at']:
                notif['received_at'] = notif['received_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({"notifications": notifications}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
