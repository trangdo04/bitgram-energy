import React, { useState } from 'react'
import Input from './components/input/input.jsx';
import LoginPopup from './components/LoginPopup/LoginPopup.jsx'
import Navbar from './components/Navbar/Navbar.jsx'
import History from './components/History/History.jsx'

import './App.css';
import { Route, Routes } from 'react-router-dom';


const App = () => {
  const [showLogin, setShowLogin] = useState(false)
  return (
    <>
      {showLogin ? <LoginPopup setShowLogin={setShowLogin} /> : <></>}
      <div className="app">
        <Navbar setShowLogin={setShowLogin} />
        <Routes>
          <Route path='/' element={<Input />} />
          <Route path='/history' element={<History />} />
        </Routes>
      </div>
    </>
  );
};

export default App;
