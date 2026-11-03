import React from "react";
import { AuthLayout } from "../components/layout/AuthLayout";
import { RegistrationForm } from "../features/authentication/RegistrationForm";
import { useLanguageStore } from "../store/useLanguageStore";

export const RegisterPage: React.FC = () => {
  const { t } = useLanguageStore();

  return (
    <AuthLayout
      title={t("auth.register.title", "Create your Exetasis account.")}
      subtitle={t(
        "auth.register.subtitle",
        "Start building an intelligent workplace environment."
      )}
    >
      <RegistrationForm />
    </AuthLayout>
  );
};

export default RegisterPage;
