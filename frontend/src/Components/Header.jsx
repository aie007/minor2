import React from 'react'
import { NavLink } from 'react-router-dom'
import Navbar from './Navbar'
import styled from 'styled-components'
import NavbarTeacher from './Navbar2'
import NavbarStudent from './Navbar3'

const Header = (props) => {
  const isLoggedIn = props.isLoggedIn;
  const isTeacher = props.isTeacher;
  if(isLoggedIn && isTeacher)
  return (
    <MainHeader>
      <NavLink to="/">
        <img src="./Images/inventory_logo.png" alt="logo" className='logo' />
      </NavLink>
      <NavbarTeacher />
      </MainHeader>
  )
  else if(isLoggedIn && !isTeacher)
  return (
    <MainHeader>
      <NavLink to="/">
        <img src="./Images/inventory_logo.png" alt="logo" className='logo' />
      </NavLink>
      <NavbarStudent />
      </MainHeader>
  )
  else
  return (
    <MainHeader>
      <NavLink to="/">
        <img src="./Images/inventory_logo.png" alt="logo" className='logo' />
      </NavLink>
      <NavbarTeacher />
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