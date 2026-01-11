use instagram;

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    type ENUM('foreground', 'background') NOT NULL,
    source VARCHAR(50) DEFAULT 'Instagram',
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_notification (title, body(255), type, source)
);
   

select * from notifications;

truncate table notifications;

