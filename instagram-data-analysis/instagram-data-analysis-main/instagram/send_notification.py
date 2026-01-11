"""
Instagram Notification Sender - Enhanced Version
Sends realistic Instagram-like push notifications with multiple features
"""

import random
import firebase_admin
from firebase_admin import credentials, messaging
import argparse
import time
from datetime import datetime
import sys

# Initialize Firebase Admin
try:
    cred = credentials.Certificate("instagram/firebase_service.json")
    firebase_admin.initialize_app(cred)
    print("✅ Firebase initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize Firebase: {e}")
    print("Please make sure 'firebase_service.json' exists and the path is correct.")
    sys.exit(1)

# Expanded notification templates with emojis
NOTIFICATION_TEMPLATES = {
    'likes': [
        "{user} liked your photo ❤️",
        "{user} liked your video 💙",
        "{user} liked your story ⭐",
        "{user} and {count} others liked your post 👍",
    ],
    'comments': [
        "{user} commented on your post 💬",
        "{user} mentioned you in a comment 📝",
        "{user} replied to your comment 💭",
        "{user} and {count} others commented on your post 🗨️",
    ],
    'follows': [
        "{user} started following you 👤",
        "{user} requested to follow you 🔔",
        "{user} accepted your follow request ✅",
    ],
    'messages': [
        "{user} sent you a message 📨",
        "{user} sent you a photo 📷",
        "{user} sent you a video 🎥",
        "{user} sent you a voice message 🎤",
        "You have {count} new messages 💌",
    ],
    'tags': [
        "{user} tagged you in a photo 🏷️",
        "{user} tagged you in a story 📸",
        "{user} mentioned you in their story 📱",
    ],
    'live': [
        "{user} started a live video 🔴",
        "{user} is live now! 📹",
    ],
    'posts': [
        "{user} shared your post 🔄",
        "{user} added your post to their story 📲",
    ],
    'activity': [
        "Your post is getting popular! 🔥",
        "You have {count} new notifications 🔔",
        "Your story has {count} views 👀",
    ]
}

# Instagram-style usernames
USERNAMES = [
    "alex_photography", "sarah_travels", "mike_fitness", "emma_foodie",
    "john_tech", "lisa_art", "david_music", "anna_fashion",
    "chris_sports", "maria_beauty", "james_gaming", "sophie_books",
    "ryan_cooking", "olivia_yoga", "daniel_cars", "emily_pets"
]

def get_random_notification():
    """Generate a random Instagram-like notification with realistic content"""
    category = random.choice(list(NOTIFICATION_TEMPLATES.keys()))
    template = random.choice(NOTIFICATION_TEMPLATES[category])
    user = random.choice(USERNAMES)
    count = random.randint(2, 50)
    
    body = template.format(user=user, count=count)
    return body, category

def send_notification(token, title, body, category=None):
    """
    Sends a push notification to a device using FCM
    
    Args:
        token: FCM device token
        title: Notification title
        body: Notification body
        category: Notification category (optional)
    """
    try:
        # Create the notification payload with additional data
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data={
                'category': category or 'general',
                'timestamp': str(int(time.time())),
                'click_action': 'FLUTTER_NOTIFICATION_CLICK'
            },
            token=token,
        )

        # Send the notification
        response = messaging.send(message)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"✅ Notification Sent Successfully!")
        print(f"{'='*60}")
        print(f"📅 Time: {timestamp}")
        print(f"📱 Title: {title}")
        print(f"💬 Body: {body}")
        print(f"🏷️  Category: {category or 'general'}")
        print(f"🆔 Message ID: {response}")
        print(f"{'='*60}\n")
        
        return response

    except Exception as e:
        print(f"\n❌ Error sending notification: {e}")
        return None

def send_bulk_notifications(token, count=5, delay=2):
    """Send multiple notifications with delay"""
    print(f"\n🚀 Sending {count} notifications with {delay}s delay...\n")
    
    success_count = 0
    for i in range(count):
        body, category = get_random_notification()
        title = "Instagram Notification"
        
        result = send_notification(token, title, body, category)
        if result:
            success_count += 1
        
        if i < count - 1:  # Don't delay after last notification
            print(f"⏳ Waiting {delay} seconds...")
            time.sleep(delay)
    
    print(f"\n📊 Summary: {success_count}/{count} notifications sent successfully")

def interactive_mode(token):
    """Interactive mode to send custom notifications"""
    print("\n" + "="*60)
    print("🎨 INTERACTIVE NOTIFICATION MODE")
    print("="*60)
    
    while True:
        print("\nOptions:")
        print("1. Send random notification")
        print("2. Send custom notification")
        print("3. Send bulk notifications")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            body, category = get_random_notification()
            send_notification(token, "Instagram Notification", body, category)
        
        elif choice == '2':
            title = input("Enter title: ").strip() or "Instagram Notification"
            body = input("Enter message: ").strip()
            if body:
                send_notification(token, title, body)
            else:
                print("❌ Message cannot be empty!")
        
        elif choice == '3':
            try:
                count = int(input("How many notifications? (1-20): ").strip())
                count = max(1, min(count, 20))  # Limit between 1-20
                delay = int(input("Delay between notifications (seconds): ").strip())
                send_bulk_notifications(token, count, delay)
            except ValueError:
                print("❌ Invalid input! Please enter numbers only.")
        
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please enter 1-4.")

def main():
    """Main function with command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Send Instagram-like push notifications via Firebase',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python send_notification.py                    # Send one random notification
  python send_notification.py --bulk 5           # Send 5 random notifications
  python send_notification.py --interactive      # Interactive mode
  python send_notification.py --custom "Hello!"  # Send custom message
        """
    )
    
    parser.add_argument('--token', type=str, 
                       default="cIXlshrNB-KT_d9CHXzDIw:APA91bFKz55oqMB5Gt59b-oPUKO_TSAVpLEAnM4DzJTUslEY3jNQQ3_QV4WXieNPJkgPZ3rEguG0ezK0f_ZOAVjPOeig0xFOtcH8O5NM4l7nY_RPpCb6zK8",
                       help='FCM device token')
    parser.add_argument('--bulk', type=int, metavar='N',
                       help='Send N random notifications')
    parser.add_argument('--delay', type=int, default=2,
                       help='Delay between bulk notifications (seconds)')
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--custom', type=str, metavar='MESSAGE',
                       help='Send custom notification message')
    parser.add_argument('--title', type=str, default='Instagram Notification',
                       help='Custom notification title')
    
    args = parser.parse_args()
    
    # Check if Firebase is initialized
    if len(firebase_admin._apps) == 0:
        print("❌ Firebase not initialized!")
        sys.exit(1)
    
    # Interactive mode
    if args.interactive:
        interactive_mode(args.token)
    
    # Bulk mode
    elif args.bulk:
        send_bulk_notifications(args.token, args.bulk, args.delay)
    
    # Custom message
    elif args.custom:
        send_notification(args.token, args.title, args.custom)
    
    # Default: send one random notification
    else:
        body, category = get_random_notification()
        send_notification(args.token, args.title, body, category)

if __name__ == "__main__":
    main()
