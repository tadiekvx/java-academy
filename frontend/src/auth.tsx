import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { api } from "./api";
import type { LearnerView } from "./types";

interface Auth {
  /** undefined while the session is being checked; null when nobody is logged in. */
  learner: LearnerView | null | undefined;
  setLearner: (learner: LearnerView | null) => void;
  logout: () => Promise<void>;
}

const AuthContext = createContext<Auth | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [learner, setLearner] = useState<LearnerView | null | undefined>(undefined);

  useEffect(() => {
    api
      .me()
      .then((me) => setLearner(me.learner))
      .catch(() => setLearner(null));
  }, []);

  const logout = useCallback(async () => {
    await api.logout();
    setLearner(null);
  }, []);

  return <AuthContext.Provider value={{ learner, setLearner, logout }}>{children}</AuthContext.Provider>;
}

export function useAuth(): Auth {
  const auth = useContext(AuthContext);
  if (!auth) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return auth;
}
