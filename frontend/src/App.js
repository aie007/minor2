// import {useEffect, useState} from 'react';
// import axios from 'axios';
// import {format} from 'date-fns';

import Navbar from "./components/Navbar";
import {BrowserRouter as Router, 
        Routes, 
        Route} from "react-router-dom";
import Home from "./pages";
import About from "./pages/about";
import Register from "./pages/register";
import Contact from "./pages/contact";

import './App.css';

// const baseUrl = "http://localhost:5000";

function App() {
  

  return (
    <Router>
      <Navbar/>
      <Routes>
        <Route exact path="/" element={<Home/>} />
        <Route path="/about" element={<About/>} />
        <Route path='/contact' element={<Contact/>} />
        <Route path='/register' element={<Register/>} />
      </Routes>
    </Router>
  );
}

export default App;
