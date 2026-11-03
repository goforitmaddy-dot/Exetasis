import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Building2, User, Mail, ShieldAlert, ArrowRight, CheckCircle2 } from "lucide-react";
import { PasswordInput } from "../../components/ui/PasswordInput";
import { SocialLoginButton } from "../../components/ui/SocialLoginButton";
import { AccountRole } from "../../services/auth";
import { useAuthStore } from "../../store/useAuthStore";
import { useLanguageStore } from "../../store/useLanguageStore";
import { cn } from "../../lib/utils";

export const RegistrationForm: React.FC = () => {
  const { t } = useLanguageStore();
  const navigate = useNavigate();
  const { register, isLoading, error: authError, clearError } = useAuthStore();

  const [accountType, setAccountType] = useState<AccountRole>("employer");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [organizationName, setOrganizationName] = useState("");
  const [invitationCode, setInvitationCode] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [success, setSuccess] = useState(false);

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!fullName.trim()) {
      newErrors.fullName = t("auth.validation.required", "This field is required.");
    }

    if (!email.trim()) {
      newErrors.email = t("auth.validation.required", "This field is required.");
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = t(
        "auth.validation.invalidEmail",
        "Please enter a valid work email address."
      );
    }

    if (accountType === "employer" && !organizationName.trim()) {
      newErrors.organizationName = t(
        "auth.validation.orgRequired",
        "Organization name is required for administrative accounts."
      );
    }

    if (accountType === "employee" && !invitationCode.trim()) {
      newErrors.invitationCode = t(
        "auth.validation.inviteRequired",
        "A valid organization invitation code is required."
      );
    }

    if (!password) {
      newErrors.password = t("auth.validation.required", "This field is required.");
    } else if (password.length < 8) {
      newErrors.password = t(
        "auth.validation.passwordLength",
        "Password must be at least 8 characters long."
      );
    }

    if (!confirmPassword) {
      newErrors.confirmPassword = t("auth.validation.required", "This field is required.");
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = t(
        "auth.validation.passwordMismatch",
        "Passwords do not match."
      );
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();

    if (!validate()) return;

    const ok = await register({
      fullName,
      email,
      password,
      accountType,
      organizationName: accountType === "employer" ? organizationName : undefined,
      invitationCode: accountType === "employee" ? invitationCode : undefined,
    });

    if (ok) {
      setSuccess(true);
      setTimeout(() => {
        navigate("/app");
      }, 1200);
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
          <span>Account created successfully! Loading your digital twin...</span>
        </div>
      )}

      {/* Account Type Selector Tabs */}
      <div className="space-y-1.5">
        <label className="block text-xs font-semibold text-slate-300">
          {t("auth.register.accountType", "Select Account Type")}
        </label>
        <div className="grid grid-cols-2 gap-2 p-1 rounded-xl bg-slate-900 border border-slate-800">
          <button
            type="button"
            onClick={() => {
              setAccountType("employer");
              setErrors((prev) => ({ ...prev, organizationName: "", invitationCode: "" }));
            }}
            className={cn(
              "flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all",
              accountType === "employer"
                ? "bg-blue-600 text-white shadow-md shadow-blue-600/30"
                : "text-slate-400 hover:text-slate-200"
            )}
          >
            <Building2 className="w-3.5 h-3.5" />
            <span className="truncate">{t("auth.register.employer", "Employer / Admin")}</span>
          </button>

          <button
            type="button"
            onClick={() => {
              setAccountType("employee");
              setErrors((prev) => ({ ...prev, organizationName: "", invitationCode: "" }));
            }}
            className={cn(
              "flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all",
              accountType === "employee"
                ? "bg-blue-600 text-white shadow-md shadow-blue-600/30"
                : "text-slate-400 hover:text-slate-200"
            )}
          >
            <User className="w-3.5 h-3.5" />
            <span className="truncate">{t("auth.register.employee", "Employee / Member")}</span>
          </button>
        </div>
      </div>

      {/* Full Name */}
      <div className="space-y-1.5">
        <label htmlFor="reg_fullname" className="block text-xs font-semibold text-slate-300">
          {t("auth.register.fullName", "Full Name")}
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
            <User className="w-4 h-4" />
          </div>
          <input
            id="reg_fullname"
            type="text"
            value={fullName}
            onChange={(e) => {
              setFullName(e.target.value);
              if (errors.fullName) setErrors((prev) => ({ ...prev, fullName: "" }));
            }}
            placeholder={t("auth.register.fullNamePlaceholder", "Sarah Jenkins")}
            className={cn(
              "w-full pl-9 pr-3 py-2.5 rounded-lg bg-slate-900/90 border text-white text-sm placeholder:text-slate-500 transition-all focus:outline-none focus:ring-2",
              errors.fullName
                ? "border-red-500/70 focus:border-red-500 focus:ring-red-500/20"
                : "border-slate-800 focus:border-blue-500 focus:ring-blue-500/30"
            )}
          />
        </div>
        {errors.fullName && <p className="text-xs text-red-400 font-medium">{errors.fullName}</p>}
      </div>

      {/* Work Email */}
      <div className="space-y-1.5">
        <label htmlFor="reg_email" className="block text-xs font-semibold text-slate-300">
          {t("auth.register.workEmail", "Work Email")}
        </label>
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
            <Mail className="w-4 h-4" />
          </div>
          <input
            id="reg_email"
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              if (errors.email) setErrors((prev) => ({ ...prev, email: "" }));
            }}
            placeholder={t("auth.register.workEmailPlaceholder", "sarah@company.com")}
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

      {/* Conditional: Organization Name if Employer */}
      {accountType === "employer" && (
        <div className="space-y-1.5 animate-in fade-in duration-200">
          <label htmlFor="reg_org_name" className="block text-xs font-semibold text-slate-300">
            {t("auth.register.orgName", "Organization Name")}
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
              <Building2 className="w-4 h-4" />
            </div>
            <input
              id="reg_org_name"
              type="text"
              value={organizationName}
              onChange={(e) => {
                setOrganizationName(e.target.value);
                if (errors.organizationName)
                  setErrors((prev) => ({ ...prev, organizationName: "" }));
              }}
              placeholder={t("auth.register.orgNamePlaceholder", "Acme Innovations Inc.")}
              className={cn(
                "w-full pl-9 pr-3 py-2.5 rounded-lg bg-slate-900/90 border text-white text-sm placeholder:text-slate-500 transition-all focus:outline-none focus:ring-2",
                errors.organizationName
                  ? "border-red-500/70 focus:border-red-500 focus:ring-red-500/20"
                  : "border-slate-800 focus:border-blue-500 focus:ring-blue-500/30"
              )}
            />
          </div>
          {errors.organizationName && (
            <p className="text-xs text-red-400 font-medium">{errors.organizationName}</p>
          )}
        </div>
      )}

      {/* Conditional: Invitation Code if Employee */}
      {accountType === "employee" && (
        <div className="space-y-1.5 animate-in fade-in duration-200">
          <label htmlFor="reg_invite_code" className="block text-xs font-semibold text-slate-300">
            {t("auth.register.inviteCode", "Organization Invitation Code")}
          </label>
          <input
            id="reg_invite_code"
            type="text"
            value={invitationCode}
            onChange={(e) => {
              setInvitationCode(e.target.value.toUpperCase());
              if (errors.invitationCode) setErrors((prev) => ({ ...prev, invitationCode: "" }));
            }}
            placeholder={t("auth.register.inviteCodePlaceholder", "EX-8849-CORP")}
            className={cn(
              "w-full px-3 py-2.5 rounded-lg bg-slate-900/90 border text-white text-sm uppercase placeholder:normal-case placeholder:text-slate-500 font-mono tracking-wider transition-all focus:outline-none focus:ring-2",
              errors.invitationCode
                ? "border-red-500/70 focus:border-red-500 focus:ring-red-500/20"
                : "border-slate-800 focus:border-blue-500 focus:ring-blue-500/30"
            )}
          />
          {errors.invitationCode && (
            <p className="text-xs text-red-400 font-medium">{errors.invitationCode}</p>
          )}
        </div>
      )}

      {/* Passwords */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <PasswordInput
          label={t("auth.register.password", "Password")}
          placeholder={t("auth.register.passwordPlaceholder", "At least 8 characters")}
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
            if (errors.password) setErrors((prev) => ({ ...prev, password: "" }));
          }}
          error={errors.password}
        />

        <PasswordInput
          label={t("auth.register.confirmPassword", "Confirm Password")}
          placeholder={t("auth.register.confirmPasswordPlaceholder", "Re-enter password")}
          value={confirmPassword}
          onChange={(e) => {
            setConfirmPassword(e.target.value);
            if (errors.confirmPassword) setErrors((prev) => ({ ...prev, confirmPassword: "" }));
          }}
          error={errors.confirmPassword}
        />
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || success}
        className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-500 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-sm shadow-xl shadow-blue-600/25 transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 active:scale-[0.99]"
      >
        <span>
          {isLoading
            ? t("auth.register.creating", "Creating Account...")
            : t("auth.register.submitBtn", "Create Account")}
        </span>
        <ArrowRight className="w-4 h-4" />
      </button>

      {/* Divider */}
      <div className="relative flex items-center justify-center my-4">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-slate-800" />
        </div>
        <span className="relative px-3 bg-[#101827] text-[11px] uppercase tracking-wider text-slate-500 font-medium">
          {t("auth.register.orContinue", "or continue with")}
        </span>
      </div>

      {/* Google SSO Button */}
      <SocialLoginButton label={t("auth.register.googleBtn", "Continue with Google")} />

      {/* Footer Link to Login */}
      <p className="text-center text-xs text-slate-400 pt-2">
        {t("auth.register.haveAccount", "Already have an account?")}{" "}
        <Link
          to="/login"
          className="text-blue-400 hover:text-blue-300 font-semibold underline underline-offset-4 decoration-blue-500/40 hover:decoration-blue-400 transition-colors"
        >
          {t("auth.register.signInLink", "Sign In")}
        </Link>
      </p>
    </form>
  );
};
