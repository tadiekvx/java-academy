// Per-browser conveniences only (unsent drafts). Storage can be unavailable or throw, so every
// access is guarded and the app works without it.

const PREFIX = "academy:";

export function loadDraft(key: string): string | null {
  try {
    return window.localStorage.getItem(PREFIX + key);
  } catch {
    return null;
  }
}

export function saveDraft(key: string, value: string): void {
  try {
    window.localStorage.setItem(PREFIX + key, value);
  } catch {
    // Not saved; the learner just loses the draft on reload.
  }
}

export function clearDraft(key: string): void {
  try {
    window.localStorage.removeItem(PREFIX + key);
  } catch {
    // Nothing to clear.
  }
}
