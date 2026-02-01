import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(localStorage.getItem('user'));

    const login = async (username, password) => {
        // Basic Auth string
        const basicAuth = 'Basic ' + btoa(username + ':' + password);
        localStorage.setItem('auth', basicAuth);
        localStorage.setItem('user', username);
        setUser(username);
        return true;
    };

    const logout = () => {
        localStorage.removeItem('auth');
        localStorage.removeItem('user');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
