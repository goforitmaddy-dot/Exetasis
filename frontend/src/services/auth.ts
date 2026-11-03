/**
 * Exetasis Authentication Service
 *
 * Current: Mock authentication client providing simulated async network delays,
 * valid payload schemas, and session tokens.
 *
 * Ready for FastAPI integration:
 * Simply toggle `USE_MOCK_AUTH = false` once FastAPI backend auth endpoints
 * (/api/auth/register, /api/auth/login, /api/auth/me) are deployed.
 */

export type AccountRole = "employer" | "employee";

export interface RegisterPayload {
  fullName: string;
  email: string;
  password: string;
  accountType: AccountRole;
  organizationName?: string;
  invitationCode?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface AuthUser {
  id: string;
  name: string;
  email: string;
  role: AccountRole;
  organizationName: string;
}

export interface AuthResponse {
  token: string;
  user: AuthUser;
  message: string;
}

const USE_MOCK_AUTH = true;
const API_BASE = "/api/auth";

class AuthService {
  /**
   * Register a new user account (Employer or Employee)
   */
  async register(payload: RegisterPayload): Promise<AuthResponse> {
    if (USE_MOCK_AUTH) {
      // Simulate network round-trip latency
      await new Promise((resolve) => setTimeout(resolve, 600));

      const mockUser: AuthUser = {
        id: `usr_${Math.random().toString(36).substring(2, 9)}`,
        name: payload.fullName,
        email: payload.email,
        role: payload.accountType,
        organizationName:
          payload.accountType === "employer"
            ? payload.organizationName || "Exetasis Enterprise"
            : `Org (${payload.invitationCode || "Linked"})`,
      };

      const token = `mock_jwt_${btoa(payload.email)}_${Date.now()}`;
      this.persistToken(token, mockUser);

      return {
        token,
        user: mockUser,
        message: "Account created successfully.",
      };
    }

    // Future FastAPI endpoint: POST /api/auth/register
    const res = await fetch(`${API_BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || "Registration failed on server.");
    }

    const data: AuthResponse = await res.json();
    this.persistToken(data.token, data.user);
    return data;
  }

  /**
   * Log into an existing account
   */
  async login(payload: LoginPayload): Promise<AuthResponse> {
    if (USE_MOCK_AUTH) {
      // Simulate network latency
      await new Promise((resolve) => setTimeout(resolve, 550));

      const mockUser: AuthUser = {
        id: "usr_mock_executive_01",
        name: payload.email.split("@")[0].replace(".", " ").replace(/\b\w/g, (c) => c.toUpperCase()),
        email: payload.email,
        role: "employer",
        organizationName: "Global Synthetics Corp",
      };

      const token = `mock_jwt_${btoa(payload.email)}_${Date.now()}`;
      this.persistToken(token, mockUser, payload.rememberMe);

      return {
        token,
        user: mockUser,
        message: "Authentication successful.",
      };
    }

    // Future FastAPI endpoint: POST /api/auth/token
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || "Invalid email or password.");
    }

    const data: AuthResponse = await res.json();
    this.persistToken(data.token, data.user, payload.rememberMe);
    return data;
  }

  logout(): void {
    try {
      localStorage.removeItem("exetasis_auth_token");
      localStorage.removeItem("exetasis_auth_user");
      sessionStorage.removeItem("exetasis_auth_token");
      sessionStorage.removeItem("exetasis_auth_user");
    } catch {
      // storage unavailable
    }
  }

  getCurrentUser(): AuthUser | null {
    try {
      const stored =
        localStorage.getItem("exetasis_auth_user") || sessionStorage.getItem("exetasis_auth_user");
      if (stored) {
        return JSON.parse(stored) as AuthUser;
      }
    } catch {
      return null;
    }
    return null;
  }

  isAuthenticated(): boolean {
    try {
      return (
        !!localStorage.getItem("exetasis_auth_token") ||
        !!sessionStorage.getItem("exetasis_auth_token")
      );
    } catch {
      return false;
    }
  }

  private persistToken(token: string, user: AuthUser, rememberMe: boolean = true): void {
    try {
      const storage = rememberMe ? localStorage : sessionStorage;
      storage.setItem("exetasis_auth_token", token);
      storage.setItem("exetasis_auth_user", JSON.stringify(user));
    } catch {
      // storage unavailable
    }
  }
}

export const authService = new AuthService();
