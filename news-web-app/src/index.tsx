import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from "react-redux";

import {store} from "./app/store"

import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics, logEvent } from "firebase/analytics";
const firebaseConfig = {
  apiKey: "AIzaSyBx1v49Beg3WQ2YHC9b-sFnhFjJG9TWlOw",
  authDomain: "news-trends-b144a.firebaseapp.com",
  projectId: "news-trends-b144a",
  storageBucket: "news-trends-b144a.firebasestorage.app",
  messagingSenderId: "931498219949",
  appId: "1:931498219949:web:02ea0cc84b212fe7102924",
  measurementId: "G-ZQZ4CPPHF0"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

logEvent(analytics, 'web_app_starts'); //빈칸있음녀 안돼요

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);


// DIF : APP 여기. 우리앱. 
root.render(
  <React.StrictMode>
  <Provider store = {store}>



    <BrowserRouter>
    
    
      
      <App /> 



    </BrowserRouter>
  </Provider>
  </React.StrictMode>
);

reportWebVitals();
