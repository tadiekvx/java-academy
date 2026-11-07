// Light by default; the learner can switch to dark. The choice is a per-browser convenience, so
// storage failures are ignored.

export type Theme = "light" | "dark";

const KEY = "academy:theme";
const listeners = new Set<(theme: Theme) => void>();

export function currentTheme(): Theme {
  return document.documentElement.dataset.theme === "dark" ? "dark" : "light";
}

export function applyStoredTheme(): void {
  let stored: string | null = null;
  try {
    stored = window.localStorage.getItem(KEY);
  } catch {
    // Storage unavailable: stay light.
  }
  document.documentElement.dataset.theme = stored === "dark" ? "dark" : "light";
}

export function setTheme(theme: Theme): void {
  document.documentElement.dataset.theme = theme;
  try {
    window.localStorage.setItem(KEY, theme);
  } catch {
    // Not remembered; fine.
  }
  listeners.forEach((listener) => listener(theme));
}

export function onThemeChange(listener: (theme: Theme) => void): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

// Apply before anything (such as the editor) reads the theme.
applyStoredTheme();
