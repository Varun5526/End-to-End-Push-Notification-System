importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js');

// Firebase configuration
const firebaseConfig = {
    // For Firebase JS SDK v7.20.0 and later, measurementId is optional
    apiKey: "AIzaSyBjgSj2nIuLtsuARzZeCWEjqNX73VdhWeE",
    authDomain: "red-plate-483805-p4.firebaseapp.com",
    projectId: "red-plate-483805-p4",
    storageBucket: "red-plate-483805-p4.firebasestorage.app",
    messagingSenderId: "465791834004",
    appId: "1:465791834004:web:915c12b0f536b569972181",
    measurementId: "G-Z96KNPDGE2"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

// Handle background notifications
messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message:', payload);

    const notificationTitle = payload.notification?.title || 'Background Notification';
    const notificationBody = payload.notification?.body || 'Background Body';

    // Display the notification
    self.registration.showNotification(notificationTitle, {
        body: notificationBody,
        icon: payload.notification?.icon || '/default-icon.png',
    });

    // Send notification data to backend for MySQL storage
    fetch('http://localhost:8000/store-notification', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: notificationTitle,
            body: notificationBody,
            type: 'background', // Indicate background notification
            source: 'Instagram', // Example source
        }),
    })
        .then((response) => response.json())
        .then((data) => console.log('Notification stored in MySQL:', data))
        .catch((error) => console.error('Error storing notification in MySQL:', error));
});
