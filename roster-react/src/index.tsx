import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import reportWebVitals from './reportWebVitals';

const domNode = document.getElementById('app');

if (domNode) {
  const accessToken = sessionStorage.getItem('access_token');

  const root = ReactDOM.createRoot(domNode);

  root.render(
    <React.StrictMode>
      <App />      
    </React.StrictMode>,
  );
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
