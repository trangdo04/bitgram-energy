import { createContext, useEffect, useState } from "react";
import axios from 'axios';
export const StoreContext = createContext(null);

const StoreContextProvider = (props) => {

    const url = "http://localhost:4000";
    const [token, setToken] = useState("");
    const [email, setEmail] = useState("");

    useEffect(()=> {
        async function loadData() {
            await fetchFoodList();
            if (localStorage.getItem("token") ) {
                setToken(localStorage.getItem("token"));
                setEmail(localStorage.getItem("email"));
                console.log()
                await loadCartData(localStorage.getItem("token"))
            }
        }
        loadData();
    },[])

    const contextValue = {
        url,
        token,
        setToken,
        email
    }

    return (
        <StoreContext.Provider value={contextValue} >
            {props.children}
        </StoreContext.Provider >
    )
}

export default StoreContextProvider;