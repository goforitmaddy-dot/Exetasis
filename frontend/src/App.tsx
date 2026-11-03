import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { WelcomePage } from "./pages/Welcome";
import { RegisterPage } from "./pages/Register";
import { LoginPage } from "./pages/Login";
import { AppWorkspace } from "./pages/AppWorkspace";

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Welcome Landing Page */}
        <Route path="/" element={<WelcomePage />} />

        {/* Create Account / Registration Page */}
        <Route path="/register" element={<RegisterPage />} />

        {/* Sign In / Login Page */}
        <Route path="/login" element={<LoginPage />} />

        {/* 3D Digital Twin & Multi-Agent Platform Workspace */}
        <Route path="/app" element={<AppWorkspace />} />
        <Route path="/dashboard" element={<Navigate to="/app" replace />} />

        {/* Fallback Catch-All Route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
