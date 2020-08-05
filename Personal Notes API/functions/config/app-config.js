// Initialize Firebase
const Firebase = require('firebase');
Firebase.initializeApp({
    apiKey: "AIzaSyDMmZjbZ4P2ha0lMxMjmCYOdglvDGpKiWg",
    authDomain: "personal-notes-2aa0a.firebaseapp.com",
    databaseURL: "https://personal-notes-2aa0a.firebaseio.com",
    projectId: "personal-notes-2aa0a",
    storageBucket: "",
    messagingSenderId: "1041128980533"
});

module.exports = Firebase;