// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyANsqwKmTSU7IWePG2iYvtw26reAdPptMI",
    authDomain: "bankrobo-39d68.firebaseapp.com",
    databaseURL: "https://bankrobo-39d68-default-rtdb.firebaseio.com",
    projectId: "bankrobo-39d68",
    storageBucket: "bankrobo-39d68.appspot.com",
    messagingSenderId: "907652973572",
    appId: "1:907652973572:web:4a386ab0a7f80989702151",
    measurementId: "G-MD52EL22ZK"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);