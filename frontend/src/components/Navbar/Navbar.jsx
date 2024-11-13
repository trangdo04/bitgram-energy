import React, { useContext, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { StoreContext } from '../../context/StoreContext.jsx';
import { assets } from '../../assets/assets.js';
import './Navbar.css'


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
                <Link to='/'><p>Home</p></Link>
                <Link to='/history'><p>History</p></Link>
            </ul>
            {!token ? <button className="sign-btn" onClick={() => setShowLogin(true)}>sign in</button>
                : <div className='navbar-profile'>
                    <img src={assets.avatar_logo} alt="" />
                    <ul className='nav-profile-dropdown'>
                        <li onClick={logout}><img src={assets.logout_icon} alt="" /><p>logout</p></li>
                    </ul>
                </div>}
        </div>
    )
};

export default Navbar;