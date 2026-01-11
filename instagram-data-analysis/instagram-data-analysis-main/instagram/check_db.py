import mysql.connector

def check_notifications():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='varun5526',
            database='instagram'
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notifications ORDER BY received_at DESC LIMIT 5")
        rows = cursor.fetchall()
        
        print(f"{'ID':<5} | {'Title':<25} | {'Body':<30} | {'Type':<12} | {'Time'}")
        print("-" * 100)
        for row in rows:
            print(f"{row['id']:<5} | {row['title']:<25} | {row['body']:<30} | {row['type']:<12} | {row['received_at']}")
            
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_notifications()
