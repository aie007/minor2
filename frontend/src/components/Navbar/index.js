import React from "react";
import {Nav, NavLink, NavMenu} from "./NavbarElements";

const Navbar = () => {
    return (
        <>
            <Nav>
                <NavMenu>
                    <NavLink to="/" activeStyle>
                        Home
                    </NavLink>
                    <NavLink to="/about" activeStyle>
                        About Us
                    </NavLink>
                    <NavLink to="/contact" activeStyle>
                        Contact
                    </NavLink>
                    <NavLink to="/register" activeStyle>
                        Register
                    </NavLink>
                </NavMenu>
            </Nav>
        </>
    );
};

export default Navbar;