// src/firebaseConfig.js
import { initializeApp } from "firebase/app";
import { getDatabase, ref, get } from "firebase/database";

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
const database = getDatabase(app);
const storage = getStorage(app);

export { database, ref, get };
