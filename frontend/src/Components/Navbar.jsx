import React from 'react'
import { NavLink } from 'react-router-dom'
import styled from 'styled-components';

const Navbar = () => {
  const Nav = styled.nav`
  .navbar-list {
    display: flex;
    gap: 4.8rem;

    li {
      list-style: none;
      .navbar-link {
        &:link,
        &:visited {
          display: inline-block;
          text-decoration: none;
          font-size: 1.8rem;
          text-transform: uppercase;
          color: ${({ theme }) => theme.colors.white};
          transition: color 0.01s linear;
        }
        &:hover,
        &:active {
          color: ${({ theme }) => theme.colors.helper};
        }
      }
    }
  }
  }


  `;
  return ( 
  <Nav>
    <div className='mecuIcon'>
      <ul className="navbar-list">

      <li>
          <NavLink className= "navbar-link" to = "/">Home</NavLink>
        </li>
        <li>
          <NavLink className= "navbar-link" to = "/register">Register</NavLink>
        </li>
        <li>
          <NavLink className= "navbar-link" to = "/about">About</NavLink>
        </li>
        <li>
          <NavLink className= "navbar-link" to = "/login">Login</NavLink>
        </li>

      </ul>
    </div>
  </Nav>
  );
  

  
}

export default Navbar