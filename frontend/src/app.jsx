import React from 'react';
import Input from './components/input';
import Output from './components/output';
import './app.css';

export function App() {
  return (
    <div className="app-container">
      <div className="input-area">
        <Input />
      </div>
      <div className="output-area">
        <Output />
      </div>
    </div>
  );
}
