import React, { useState, useEffect } from 'react'
import About from './About'
import Home from './Home'
import Login from './Login'
import Register from './Register'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from './Components/Header';
import Footer from './Components/Footer';
import { ThemeProvider } from "styled-components"
import { GlobalStyle } from './GlobalStyle';
// import axios from "axios";

const App = () => {

  const theme = {
    colors: {
      heading: "rgb(24 24 29)",
      text: "rgb(24 24 29)",
      white: "#fff",
      black: " #212529",
      helper: "#8490ff",
      bg: "rgb(113 112 117)",
      footer_bg: "#0a1435",
      btn: "rgb(98 84 243)",
      border: "rgba(98, 84, 243, 0.5)",
      hr: "#ffffff",
      gradient:
        "linear-gradient(0deg, rgb(132 144 255) 0%, rgb(98 189 252) 100%)",
      shadow:
        "rgba(0, 0, 0, 0.02) 0px 1px 3px 0px,rgba(27, 31, 35, 0.15) 0px 0px 0px 1px;",
      shadowSupport: " rgba(0, 0, 0, 0.16) 0px 1px 4px",
    },
    media: { mobile: "768px", tab: "998px" },
  };

  return (
  <ThemeProvider theme = {theme}>
  <GlobalStyle />
   <BrowserRouter>
   <Header />
   <Routes>
    <Route path="/" element={<Home />} />
    <Route path='/register' element={<Register />} />
    <Route path="/login" element={<Login />} />
    <Route path="/about" element={<About />} />
   </Routes>
   {/* <div> <p>To get your profile details: </p><button onClick={getData}>Click me</button>
        {profileData && <div>
              <p>Profile name: {profileData.profile_name}</p>
              <p>About me: {profileData.about_me}</p>
            </div>
        } </div> */}
   <Footer />
   </BrowserRouter>
  </ThemeProvider>
   
  );
};

export default App