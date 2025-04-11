import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";  // Add this import

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCPkPdXeKOjC7g3QUT8RCYYskrgZxVC5iE",
  authDomain: "abc123-b25e0.firebaseapp.com",
  projectId: "abc123-b25e0",
  storageBucket: "abc123-b25e0.firebasestorage.app",
  messagingSenderId: "342119378472",
  appId: "1:342119378472:web:678370800bd0df02c80f1d",
  measurementId: "G-F3EF0B0Q6M"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);  // Add this export