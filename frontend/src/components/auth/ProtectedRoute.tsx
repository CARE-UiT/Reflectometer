import React, { useContext, useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import axios from 'axios';
import { UserContext } from '../../contexts/user';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const { user, setUser } = useContext(UserContext);
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const validateToken = async () => {
            const token = localStorage.getItem('token') || sessionStorage.getItem('token');
            if (token) {
                try {
                    const response = await axios.get('/api/auth/current', {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    });
                    setUser({ email: response.data.email });
                    setIsAuthenticated(true);
                } catch (error) {
                    console.error('Invalid token:', error);
                    localStorage.removeItem('token');
                    sessionStorage.removeItem('token');
                    setIsAuthenticated(false);
                }
            } else {
                setIsAuthenticated(false);
            }
            setLoading(false);
        };

        validateToken();
    }, [setUser]);

    if (loading) {
        return <div>Loading...</div>; // You could replace this with a spinner or other loading component
    }

    if (!isAuthenticated) {
        return <Navigate to="/signin" replace />;
    }

    return <>{children}</>;
};

export default ProtectedRoute;
