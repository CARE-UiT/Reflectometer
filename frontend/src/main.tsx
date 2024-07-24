import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import ErrorPage from './pages/errorPage.tsx';
import SignInSide from './pages/signin.tsx';
import LandingPage from './pages/landingPage.tsx';
import SignUp from './pages/signup.tsx';
import { MyPage } from './pages/mypage.tsx';
import { ReflectometerPage } from './pages/reflectometer.tsx';
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
    path: "mypage",
    element: <App> <MyPage /> </App>,
  },
  {
    path: "reflectometer/:id",
    element: <App><ReflectometerPage /></App>
  }
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)