import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import ErrorPage from './pages/errorPage.tsx';
import SignInSide from './pages/signin.tsx';
import LandingPage from './pages/landingPage.tsx';
import SignUp from './pages/signup.tsx';
import { ReflectometerPage } from './pages/reflectometer.tsx';
import Dashboard from './components/dashboard/Dashboard.tsx';
import { UserProvider } from './contexts/user.tsx';
import axios from 'axios';
import ProtectedRoute from './components/auth/ProtectedRoute.tsx';

axios.defaults.baseURL = 'http://localhost:8080';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App> <LandingPage /> </App>,
    errorElement: <ErrorPage />,
  },
  {
    path: "signin",
    element: <SignInSide />,
  },
  {
    path: "signup",
    element: <SignUp />,
  },
  {
    path: "reflectometer/:id",
    element: <App><ReflectometerPage /></App>
  },
  {
    path: "instructor",
    element: (
      <ProtectedRoute>
        <App>
          <Dashboard />
        </App>
      </ProtectedRoute>
    ),
  }
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <UserProvider>
      <RouterProvider router={router} />
    </UserProvider>
  </React.StrictMode>
);
