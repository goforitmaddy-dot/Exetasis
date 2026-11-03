import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Mail, ShieldAlert, ArrowRight, CheckCircle2 } from "lucide-react";
import { PasswordInput } from "../../components/ui/PasswordInput";
import { SocialLoginButton } from "../../components/ui/SocialLoginButton";
import { useAuthStore } from "../../store/useAuthStore";
import { useLanguageStore } from "../../store/useLanguageStore";
import { cn } from "../../lib/utils";

export const LoginForm: React.FC = () => {
  const { t } = useLanguageStore();
  const navigate = useNavigate();
  const { login, isLoading, error: authError, clearError } = useAuthStore();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(true);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [success, setSuccess] = useState(false);

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!email.trim()) {
      newErrors.email = t("auth.validation.required", "This field is required.");
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = t(
        "auth.validation.invalidEmail",
        "Please enter a valid work email address."
      );
    }

    if (!password) {
      newErrors.password = t("auth.validation.required", "This field is required.");
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();

    if (!validate()) return;

    const ok = await login({ email, password, rememberMe });
    if (ok) {
      setSuccess(true);
      setTimeout(() => {
        navigate("/app");
      }, 1000);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5" noValidate>
      {authError && (
        <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 flex-shrink-0" />
          <span>{authError}</span>
        </div>
      )}

      {success && (
        <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          <span>Authentication successful. Loading workspace...</span>
        </div>
      )}

      {/* Work Email */}
      <div className="space-y-1.5">
        <label htmlFor="login_email" className="block text-xs font-semibold text-slate-300">
          {t("auth.login.workEmail", "Work Email")}
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
            <Mail className="w-4 h-4" />
          </div>
          <input
            id="login_email"
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              if (errors.email) setErrors((prev) => ({ ...prev, email: "" }));
            }}
            placeholder={t("auth.login.workEmailPlaceholder", "you@company.com")}
            className={cn(
              "w-full pl-9 pr-3 py-2.5 rounded-lg bg-slate-900/90 border text-white text-sm placeholder:text-slate-500 transition-all focus:outline-none focus:ring-2",
              errors.email
                ? "border-red-500/70 focus:border-red-500 focus:ring-red-500/20"
                : "border-slate-800 focus:border-blue-500 focus:ring-blue-500/30"
            )}
          />
        </div>
        {errors.email && <p className="text-xs text-red-400 font-medium">{errors.email}</p>}
      </div>

      {/* Password with Show/Hide Toggle */}
      <div className="space-y-1.5">
        <PasswordInput
          label={t("auth.login.password", "Password")}
          placeholder={t("auth.login.passwordPlaceholder", "Enter your password")}
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
            if (errors.password) setErrors((prev) => ({ ...prev, password: "" }));
          }}
          error={errors.password}
        />
      </div>

      {/* Remember Me & Forgot Password Row */}
      <div className="flex items-center justify-between text-xs">
        <label className="flex items-center gap-2 cursor-pointer text-slate-300 select-none">
          <input
            type="checkbox"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
            className="w-4 h-4 rounded border-slate-700 bg-slate-900 text-blue-600 focus:ring-blue-500/40"
          />
          <span>{t("auth.login.rememberMe", "Remember this device")}</span>
        </label>

        <button
          type="button"
          onClick={() => alert("Password reset workflow is connected via workplace administrator.")}
          className="text-blue-400 hover:text-blue-300 font-medium transition-colors"
        >
          {t("auth.login.forgotPassword", "Forgot password?")}
        </button>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || success}
        className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-500 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-sm shadow-xl shadow-blue-600/25 transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 active:scale-[0.99]"
      >
        <span>
          {isLoading
            ? t("auth.login.signingIn", "Authenticating...")
            : t("auth.login.submitBtn", "Sign In")}
        </span>
        <ArrowRight className="w-4 h-4" />
      </button>

      {/* Divider */}
      <div className="relative flex items-center justify-center my-4">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-slate-800" />
        </div>
        <span className="relative px-3 bg-[#101827] text-[11px] uppercase tracking-wider text-slate-500 font-medium">
          {t("auth.login.orContinue", "or continue with")}
        </span>
      </div>

      {/* Google SSO Button */}
      <SocialLoginButton label={t("auth.login.googleBtn", "Continue with Google")} />

      {/* Footer Link to Register */}
      <p className="text-center text-xs text-slate-400 pt-2">
        {t("auth.login.noAccount", "Don't have an account?")}{" "}
        <Link
          to="/register"
          className="text-blue-400 hover:text-blue-300 font-semibold underline underline-offset-4 decoration-blue-500/40 hover:decoration-blue-400 transition-colors"
        >
          {t("auth.login.createAccountLink", "Create an account")}
        </Link>
      </p>
    </form>
  );
};
