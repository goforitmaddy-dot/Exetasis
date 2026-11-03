import React from "react";
import { AuthLayout } from "../components/layout/AuthLayout";
import { LoginForm } from "../features/authentication/LoginForm";
import { useLanguageStore } from "../store/useLanguageStore";

export const LoginPage: React.FC = () => {
  const { t } = useLanguageStore();

  return (
    <AuthLayout
      title={t("auth.login.title", "Welcome back to Exetasis.")}
      subtitle={t(
        "auth.login.subtitle",
        "Sign in to access your workplace intelligence twin."
      )}
    >
      <LoginForm />
    </AuthLayout>
  );
};

export default LoginPage;
