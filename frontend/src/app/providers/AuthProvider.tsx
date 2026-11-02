import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { me, User } from "@/features/auth/api/auth";

interface AuthContextType {
  token: string | null;
  user: User | null;
  login: (token: string, user?: User) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("shopflow_token");
    }
    return null;
  });
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    if (token) {
      localStorage.setItem("shopflow_token", token);
      me()
        .then((u) => setUser(u))
        .catch(() => {
          localStorage.removeItem("shopflow_token");
          setToken(null);
          setUser(null);
        });
    } else {
      localStorage.removeItem("shopflow_token");
      setUser(null);
    }
  }, [token]);

  const login = (t: string, u?: User) => {
    localStorage.setItem("shopflow_token", t);
    if (u) setUser(u);
    setToken(t);
  };

  const logout = () => {
    localStorage.removeItem("shopflow_token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
