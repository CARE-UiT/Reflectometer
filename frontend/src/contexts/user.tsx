import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

interface User {
    email: string | null;
}

interface UserContextProps {
    user: User;
    setUser: (user: User) => void;
}

export const UserContext = createContext<UserContextProps>({
    user: { email: null },
    setUser: () => { },
});

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User>({ email: null });

    useEffect(() => {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        if (token) {
            axios.get('/api/auth/current', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    setUser({ email: response.data.email });
                })
                .catch(error => {
                    console.error('Failed to fetch user information:', error);
                    // If there's an error (e.g., token is invalid), clear the stored token
                    localStorage.removeItem('token');
                    sessionStorage.removeItem('token');
                    setUser({ email: null });
                });
        }
    }, []);

    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
};
