import { create } from "zustand";
import { authService, AuthUser, LoginPayload, RegisterPayload } from "../services/auth";

interface AuthState {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  register: (payload: RegisterPayload) => Promise<boolean>;
  login: (payload: LoginPayload) => Promise<boolean>;
  logout: () => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: authService.getCurrentUser(),
  isAuthenticated: authService.isAuthenticated(),
  isLoading: false,
  error: null,

  register: async (payload: RegisterPayload) => {
    set({ isLoading: true, error: null });
    try {
      const res = await authService.register(payload);
      set({ user: res.user, isAuthenticated: true, isLoading: false });
      return true;
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : "Failed to register account",
        isLoading: false,
      });
      return false;
    }
  },

  login: async (payload: LoginPayload) => {
    set({ isLoading: true, error: null });
    try {
      const res = await authService.login(payload);
      set({ user: res.user, isAuthenticated: true, isLoading: false });
      return true;
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : "Invalid credentials",
        isLoading: false,
      });
      return false;
    }
  },

  logout: () => {
    authService.logout();
    set({ user: null, isAuthenticated: false, error: null });
  },

  clearError: () => set({ error: null }),
}));
