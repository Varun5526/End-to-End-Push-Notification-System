# End-to-End-Push-Notification-System
I designed and built an end-to-end push notification system to understand how real-world applications (like Instagram or e-commerce platforms) handle notifications behind the scenes.
# 🔔 How the Instagram Notification System Works

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Step-by-Step Process](#step-by-step-process)
5. [Technology Stack](#technology-stack)
6. [Database Schema](#database-schema)

---

## 🎯 System Overview

This is a **real-time push notification system** that mimics Instagram's notification functionality. It allows you to:
- Send push notifications to web browsers
- Store notification history in a database
- Analyze notification patterns
- Display notifications in real-time

### Key Features:
✅ Real-time push notifications via Firebase Cloud Messaging (FCM)  
✅ Foreground & Background notification handling  
✅ MySQL database storage for analytics  
✅ Beautiful web dashboard  
✅ Data visualization and reporting  

---

## 🏗️ Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM COMPONENTS                         │
└─────────────────────────────────────────────────────────────┘

1. FRONTEND (index.html)
   ├── User Interface (HTML/CSS)
   ├── Firebase SDK (JavaScript)
   └── Service Worker Registration

2. SERVICE WORKER (firebase.js)
   ├── Background Message Handler
   └── Notification Display Logic

3. BACKEND (app.py - Flask)
   ├── API Endpoints
   ├── Database Connection
   └── CORS Configuration

4. DATABASE (MySQL)
   ├── notifications table
   └── Stores all notification history

5. NOTIFICATION SENDER (send_notification.py)
   ├── Firebase Admin SDK
   ├── Notification Templates
   └── Bulk Sending Logic

6. ANALYTICS (analytics.py)
   ├── Data Queries
   ├── Chart Generation
   └── Report Export
```

---

## 🔄 Data Flow

### **Flow 1: User Enables Notifications**

```
┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│  User    │─────▶│ Browser  │─────▶│ Firebase │─────▶│  Server  │
│ (Client) │      │  (FCM)   │      │   SDK    │      │  (Flask) │
└──────────┘      └──────────┘      └──────────┘      └──────────┘
     │                  │                  │                  │
     │ 1. Click        │                  │                  │
     │ "Enable"        │                  │                  │
     │                 │                  │                  │
     │                 │ 2. Request       │                  │
     │                 │ Permission       │                  │
     │                 │                  │                  │
     │                 │ 3. Register      │                  │
     │                 │ Service Worker   │                  │
     │                 │                  │                  │
     │                 │                  │ 4. Generate      │
     │                 │                  │ FCM Token        │
     │                 │                  │                  │
     │ 5. Display      │◀─────────────────┤                  │
     │ Token           │                  │                  │
     └─────────────────┴──────────────────┴──────────────────┘
```

### **Flow 2: Sending a Notification**

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Python Script│─────▶│   Firebase   │─────▶│   Browser    │
│send_notif.py │      │  Cloud (FCM) │      │   (Client)   │
└──────────────┘      └──────────────┘      └──────────────┘
       │                      │                      │
       │ 1. Create           │                      │
       │ Message             │                      │
       │ + Token             │                      │
       │                     │                      │
       │ 2. Send via         │                      │
       │ Admin SDK           │                      │
       │                     │                      │
       │                     │ 3. Route to          │
       │                     │ Device               │
       │                     │                      │
       │                     │                      │ 4a. Foreground
       │                     │                      │ → onMessage()
       │                     │                      │
       │                     │                      │ 4b. Background
       │                     │                      │ → Service Worker
       │                     │                      │
       └─────────────────────┴──────────────────────┘
```

### **Flow 3: Storing Notification in Database**

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Browser    │─────▶│ Flask Server │─────▶│    MySQL     │
│  (Client)    │      │   (app.py)   │      │  Database    │
└──────────────┘      └──────────────┘      └──────────────┘
       │                     │                      │
       │ 1. Receive          │                      │
       │ Notification        │                      │
       │                     │                      │
       │ 2. POST to          │                      │
       │ /store-notification │                      │
       │                     │                      │
       │                     │ 3. INSERT INTO       │
       │                     │ notifications        │
       │                     │                      │
       │                     │                      │ 4. Store
       │                     │                      │ Record
       │                     │                      │
       │ 5. Return           │◀───────────────── ───┤
       │ Success             │                      │
       └─────────────────────┴──────────────────────┘
```

---

## 📝 Step-by-Step Process

### **Phase 1: Setup & Initialization**

1. **User Opens Website** (`http://localhost:8000`)
   - Browser loads `index.html`
   - Firebase SDK initializes
   - Page fetches total notification count from database

2. **User Clicks "Enable Notifications"**
   - Browser requests notification permission
   - User grants permission
   - Service Worker registers (`firebase.js`)
   - FCM generates unique device token
   - Token displayed on screen

### **Phase 2: Sending Notifications**

3. **Run Python Script**
   ```bash
   python instagram/send_notification.py
   ```
   - Script loads Firebase Admin credentials
   - Generates random notification (or custom)
   - Sends to Firebase Cloud Messaging
   - FCM routes to specific device using token

4. **Firebase Delivers Notification**
   - If browser is **open (foreground)**:
     - `messaging.onMessage()` fires in `index.html`
     - Shows system notification
     - Adds to notification list
     - Sends to backend API
   
   - If browser is **closed (background)**:
     - Service Worker (`firebase.js`) receives it
     - Shows system notification
     - Sends to backend API

### **Phase 3: Storage & Display**

5. **Backend Stores Notification**
   - Flask receives POST request at `/store-notification`
   - Extracts: title, body, type, source
   - Inserts into MySQL database
   - Returns success response

6. **Frontend Updates**
   - Notification appears in list with timestamp
   - Session counter increments
   - Total counter updates

### **Phase 4: Analytics**

7. **Generate Analytics**
   ```bash
   python instagram/analytics.py
   ```
   - Connects to MySQL database
   - Runs SQL queries from `inta analyst.sql`
   - Generates charts (matplotlib/seaborn)
   - Exports CSV reports
   - Saves to `analytics_output/` folder

---

## 🛠️ Technology Stack

### **Frontend**
- **HTML5** - Structure
- **CSS3** - Styling (Instagram gradient theme)
- **JavaScript** - Logic & Firebase integration
- **Firebase SDK 8.10.0** - Cloud Messaging

### **Backend**
- **Python 3.11** - Programming language
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin requests
- **mysql-connector-python** - Database driver

### **Database**
- **MySQL** - Relational database
- **Schema**: notifications table

### **Notification Service**
- **Firebase Cloud Messaging (FCM)** - Push notifications
- **Firebase Admin SDK** - Server-side sending
- **Service Workers** - Background processing

### **Analytics**
- **Pandas** - Data manipulation
- **Matplotlib** - Chart generation
- **Seaborn** - Statistical visualization

---

## 🗄️ Database Schema

```sql
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    type ENUM('foreground', 'background') NOT NULL,
    source VARCHAR(50) DEFAULT 'Instagram',
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_notification (title, body(255), type, source)
);
```

### **Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | INT | Auto-incrementing primary key |
| `title` | VARCHAR(255) | Notification title (e.g., "Instagram Notification") |
| `body` | TEXT | Notification message (e.g., "user1 liked your photo") |
| `type` | ENUM | Either 'foreground' or 'background' |
| `source` | VARCHAR(50) | Source app (default: 'Instagram') |
| `received_at` | TIMESTAMP | When notification was received |

### **Unique Constraint:**
Prevents duplicate notifications with same title, body, type, and source.

---

## 🔐 Security & Configuration

### **Firebase Configuration**
Located in `firebase_service.json`:
- Project ID
- Private key
- Client email
- Service account credentials

### **Database Credentials**
In `app.py`:
```python
host='localhost'
user='root'
password='varun5526'
database='instagram'
```

### **FCM Token**
Unique per device/browser. Example:
```
dpWy_suyEcydd9rx4TiS8M:APA91bG7ChiP3ysiACitKABp...
```

---

## 📊 API Endpoints

### **1. Store Notification**
```
POST /store-notification
Content-Type: application/json

{
  "title": "Instagram Notification",
  "body": "user1 liked your photo",
  "type": "foreground",
  "source": "Instagram"
}

Response: {"message": "Notification stored successfully"}
```

### **2. Get Notification Count**
```
GET /notification-count

Response: {"total": 5}
```

### **3. Serve Frontend**
```
GET /

Response: index.html (rendered page)
```

---

## 🎨 User Interface Components

### **Dashboard Elements:**
1. **Header** - Logo, title, subtitle
2. **Enable Button** - Activates notifications
3. **Status Badge** - Shows enabled/disabled state
4. **Token Display** - Shows FCM token with copy button
5. **Statistics Cards** - Total & session counts
6. **Notification List** - Recent notifications with timestamps
7. **Clear Button** - Removes all from list

### **Visual Features:**
- Instagram gradient (purple to pink)
- Smooth animations
- Toast notifications
- Loading spinners
- Responsive design

---

## 🔍 How Each File Works

### **1. index.html**
- Displays the web interface
- Handles user interactions
- Manages Firebase messaging
- Updates UI in real-time

### **2. firebase.js** (Service Worker)
- Runs in background
- Receives notifications when browser is closed
- Shows system notifications
- Sends data to backend

### **3. app.py** (Flask Server)
- Serves the frontend
- Provides API endpoints
- Connects to MySQL
- Handles CORS

### **4. send_notification.py**
- Sends notifications via Firebase Admin SDK
- Generates random realistic messages
- Supports bulk sending
- Interactive mode

### **5. analytics.py**
- Queries database
- Generates visualizations
- Exports reports
- Creates charts

### **6. check_db.py**
- Simple utility to view notifications
- Displays last 5 entries
- Formatted table output

---

## 🚀 Quick Start Guide

1. **Start Backend:**
   ```bash
   python instagram/app.py
   ```

2. **Open Browser:**
   ```
   http://localhost:8000
   ```

3. **Enable Notifications:**
   - Click button
   - Grant permission
   - Copy token

4. **Send Notification:**
   ```bash
   python instagram/send_notification.py
   ```

5. **View Analytics:**
   ```bash
   python instagram/analytics.py
   ```

---

## 🎯 Real-World Use Cases

1. **Social Media Apps** - User engagement notifications
2. **E-commerce** - Order updates, promotions
3. **News Apps** - Breaking news alerts
4. **Messaging Apps** - New message notifications
5. **Gaming** - Achievement unlocks
6. **Productivity** - Task reminders

---

## 📈 Analytics Capabilities

The system can analyze:
- Notification frequency by hour/day
- Foreground vs background distribution
- Most common notification types
- Peak activity times
- User engagement patterns
- Daily/weekly trends

---

## 🎓 Learning Outcomes

By building this system, you learn:
- ✅ Push notification architecture
- ✅ Service Worker implementation
- ✅ Real-time web applications
- ✅ RESTful API design
- ✅ Database integration
- ✅ Data visualization
- ✅ Full-stack development

---

## 📚 Additional Resources

- [Firebase Cloud Messaging Docs](https://firebase.google.com/docs/cloud-messaging)
- [Service Workers Guide](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MySQL Tutorial](https://dev.mysql.com/doc/)

---

**Created by:** Varun  
**Project:** Instagram Notification System  
**Date:** January 2026  
**Version:** 2.0
