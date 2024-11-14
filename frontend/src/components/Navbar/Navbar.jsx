import React, { useContext, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { StoreContext } from '../../context/StoreContext.jsx';
import { assets } from '../../assets/assets.js';
import './Navbar.css'
import { NavLink } from 'react-router-dom';

const Navbar = ({ setShowLogin }) => {
    const { token, setToken } = useContext(StoreContext);
    const navigate = useNavigate();

    useEffect(() => {
        const storedToken = localStorage.getItem("token");
        if (storedToken && !token) {
            setToken(storedToken);
        }
    }, [token, setToken]);

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("email");
        localStorage.removeItem("name");
        setToken("");
        navigate("/");
    };

    return (
        <div className='navbar'>
            <ul className="navbar-menu">
                <NavLink
                    to="/"
                    className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
                >
                    <p><img src={assets.home_icon} alt="Home Icon" className="icon-image" /> Home</p>
                </NavLink>
                <NavLink
                    to="/history"
                    className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
                >
                    <p><img src={assets.history_icon} alt="History Icon" className="icon-image" /> History</p>
                </NavLink>
            </ul>
            {!token ? (<button className="sign-btn" onClick={() => setShowLogin(true)}>
                <img src={assets.signin_icon} alt="Sign In Icon" className="icon-image" />
                Sign in
            </button>)
                : (<div className='navbar-profile'>
                    <img src={assets.avatar_logo} alt="" className='profile' />
                    <ul className='nav-profile-dropdown'>
                        <li onClick={logout}><img src={assets.logout_icon} alt="" className='logout_icon' /><p>Logout</p></li>
                    </ul>
                </div>)}
        </div>
    )
};

export default Navbar;