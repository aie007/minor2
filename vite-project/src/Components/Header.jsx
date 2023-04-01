import React from 'react'
import { NavLink } from 'react-router-dom'
import Navbar from './Navbar'
import styled from 'styled-components'
import Home from '../Home'
const Header = () => {
  return (

    <MainHeader>
      <NavLink to="/">
        <img src="./Images/inventory_logo.png" alt="logo" className='logo' />
      </NavLink>

      <div>
        <NavLink to="/home">
          Home
        </NavLink>
      </div>
      <Navbar />
      </MainHeader>
    
  )
  }

  const MainHeader = styled.header`
  padding: 0 4.8rem;
  height: 10rem;
  background-color: ${({ theme }) => theme.colors.bg};
  display: flex;
  justify-content: space-between;
  align-items: center;

  .logo {
    height: auto;
    max-width: 30%;
  }
  `;

export default Header