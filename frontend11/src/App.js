import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/landing/LandingPage';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import DashboardLayout from './components/shared/DashboardLayout';
import UploadPage from './pages/dashboard/upload/UploadPage';
import MyCreationsPage from './pages/dashboard/creations/MyCreationsPage';
import VerifyPage from './pages/dashboard/verify/VerifyPage';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <DashboardLayout />
            </PrivateRoute>
          }
        >
          <Route path="upload" element={<UploadPage />} />
          <Route path="creations" element={<MyCreationsPage />} />
          <Route path="verify" element={<VerifyPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
