import { createContext, useContext, useEffect, useState, ReactNode } from "react";

interface AuthContextType {
  token: string | null;
  user: any | null;
  login: (token: string) => void;
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
  const [user, setUser] = useState<any | null>(null);

  useEffect(() => {
    if (token) {
      localStorage.setItem("shopflow_token", token);
    } else {
      localStorage.removeItem("shopflow_token");
    }
  }, [token]);

  const login = (t: string) => setToken(t);
  const logout = () => {
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
