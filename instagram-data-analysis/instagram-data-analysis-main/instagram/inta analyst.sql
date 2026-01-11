-- ============================================
-- Instagram Notification Analytics
-- Data Analysis for Instagram Notification System
-- ============================================

USE instagram;

-- ============================================
-- 1. BASIC STATISTICS
-- ============================================

-- Total notifications count
SELECT COUNT(*) AS total_notifications
FROM notifications;

-- Notifications by type (foreground vs background)
SELECT 
    type,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM notifications), 2) AS percentage
FROM notifications
GROUP BY type
ORDER BY count DESC;

-- Notifications by source
SELECT 
    source,
    COUNT(*) AS count
FROM notifications
GROUP BY source
ORDER BY count DESC;

-- ============================================
-- 2. TIME-BASED ANALYSIS
-- ============================================

-- Notifications per hour of day
SELECT 
    HOUR(received_at) AS hour_of_day,
    COUNT(*) AS notification_count,
    ROUND(AVG(COUNT(*)) OVER(), 2) AS avg_per_hour
FROM notifications
GROUP BY HOUR(received_at)
ORDER BY hour_of_day;

-- Notifications per day of week
SELECT 
    DAYNAME(received_at) AS day_of_week,
    COUNT(*) AS notification_count
FROM notifications
GROUP BY DAYNAME(received_at), DAYOFWEEK(received_at)
ORDER BY DAYOFWEEK(received_at);

-- Daily notification trend (last 7 days)
SELECT 
    DATE(received_at) AS notification_date,
    COUNT(*) AS daily_count,
    type,
    COUNT(*) OVER (PARTITION BY DATE(received_at)) AS total_per_day
FROM notifications
WHERE received_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY DATE(received_at), type
ORDER BY notification_date DESC, type;

-- ============================================
-- 3. NOTIFICATION CONTENT ANALYSIS
-- ============================================

-- Most common notification titles
SELECT 
    title,
    COUNT(*) AS frequency,
    MIN(received_at) AS first_occurrence,
    MAX(received_at) AS last_occurrence
FROM notifications
GROUP BY title
ORDER BY frequency DESC
LIMIT 10;

-- Most common notification bodies (actions)
SELECT 
    body,
    COUNT(*) AS frequency,
    type
FROM notifications
GROUP BY body, type
ORDER BY frequency DESC
LIMIT 10;

-- Unique notification patterns
SELECT 
    CONCAT(title, ' - ', body) AS notification_pattern,
    COUNT(*) AS occurrences,
    type
FROM notifications
GROUP BY title, body, type
ORDER BY occurrences DESC;

-- ============================================
-- 4. ENGAGEMENT PATTERNS
-- ============================================

-- Peak notification hours
SELECT 
    HOUR(received_at) AS peak_hour,
    COUNT(*) AS notification_count,
    CASE 
        WHEN HOUR(received_at) BETWEEN 6 AND 11 THEN 'Morning'
        WHEN HOUR(received_at) BETWEEN 12 AND 17 THEN 'Afternoon'
        WHEN HOUR(received_at) BETWEEN 18 AND 23 THEN 'Evening'
        ELSE 'Night'
    END AS time_period
FROM notifications
GROUP BY HOUR(received_at)
ORDER BY notification_count DESC
LIMIT 5;

-- Average notifications per day
SELECT 
    ROUND(COUNT(*) / COUNT(DISTINCT DATE(received_at)), 2) AS avg_notifications_per_day,
    COUNT(DISTINCT DATE(received_at)) AS total_days,
    COUNT(*) AS total_notifications
FROM notifications;

-- ============================================
-- 5. RECENT ACTIVITY
-- ============================================

-- Last 10 notifications
SELECT 
    id,
    title,
    body,
    type,
    received_at,
    TIMESTAMPDIFF(MINUTE, received_at, NOW()) AS minutes_ago
FROM notifications
ORDER BY received_at DESC
LIMIT 10;

-- Notifications received today
SELECT 
    COUNT(*) AS today_count,
    type,
    MIN(received_at) AS first_today,
    MAX(received_at) AS last_today
FROM notifications
WHERE DATE(received_at) = CURDATE()
GROUP BY type;

-- ============================================
-- 6. ADVANCED ANALYTICS
-- ============================================

-- Notification frequency by hour and type
SELECT 
    HOUR(received_at) AS hour,
    type,
    COUNT(*) AS count
FROM notifications
GROUP BY HOUR(received_at), type
ORDER BY hour, type;

-- Time gaps between notifications (in minutes)
SELECT 
    n1.id,
    n1.title,
    n1.received_at,
    TIMESTAMPDIFF(MINUTE, 
        LAG(n1.received_at) OVER (ORDER BY n1.received_at), 
        n1.received_at
    ) AS minutes_since_last
FROM notifications n1
ORDER BY n1.received_at DESC
LIMIT 20;

-- Busiest days (top 5)
SELECT 
    DATE(received_at) AS busy_date,
    COUNT(*) AS notification_count,
    GROUP_CONCAT(DISTINCT type) AS notification_types
FROM notifications
GROUP BY DATE(received_at)
ORDER BY notification_count DESC
LIMIT 5;

-- ============================================
-- 7. NOTIFICATION TYPE COMPARISON
-- ============================================

-- Foreground vs Background comparison
SELECT 
    'Foreground' AS notification_type,
    COUNT(*) AS total,
    ROUND(AVG(TIMESTAMPDIFF(SECOND, 
        LAG(received_at) OVER (PARTITION BY type ORDER BY received_at), 
        received_at
    )), 2) AS avg_gap_seconds
FROM notifications
WHERE type = 'foreground'

UNION ALL

SELECT 
    'Background' AS notification_type,
    COUNT(*) AS total,
    ROUND(AVG(TIMESTAMPDIFF(SECOND, 
        LAG(received_at) OVER (PARTITION BY type ORDER BY received_at), 
        received_at
    )), 2) AS avg_gap_seconds
FROM notifications
WHERE type = 'background';

-- ============================================
-- 8. SUMMARY DASHBOARD QUERY
-- ============================================

-- Comprehensive summary for dashboard
SELECT 
    (SELECT COUNT(*) FROM notifications) AS total_notifications,
    (SELECT COUNT(*) FROM notifications WHERE type = 'foreground') AS foreground_count,
    (SELECT COUNT(*) FROM notifications WHERE type = 'background') AS background_count,
    (SELECT COUNT(*) FROM notifications WHERE DATE(received_at) = CURDATE()) AS today_count,
    (SELECT COUNT(*) FROM notifications WHERE received_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)) AS last_7_days,
    (SELECT COUNT(DISTINCT DATE(received_at)) FROM notifications) AS active_days,
    (SELECT MAX(received_at) FROM notifications) AS last_notification,
    (SELECT MIN(received_at) FROM notifications) AS first_notification;

-- ============================================
-- 9. EXPORT QUERIES FOR VISUALIZATION
-- ============================================

-- Data for time series chart (hourly distribution)
SELECT 
    DATE_FORMAT(received_at, '%Y-%m-%d %H:00:00') AS hour_bucket,
    COUNT(*) AS notification_count,
    type
FROM notifications
GROUP BY DATE_FORMAT(received_at, '%Y-%m-%d %H:00:00'), type
ORDER BY hour_bucket;

-- Data for pie chart (notification types)
SELECT 
    type AS label,
    COUNT(*) AS value
FROM notifications
GROUP BY type;

-- Data for bar chart (top notification actions)
SELECT 
    body AS action,
    COUNT(*) AS count
FROM notifications
GROUP BY body
ORDER BY count DESC
LIMIT 10;
