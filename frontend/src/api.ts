import type {
  AttemptContext,
  CurriculumView,
  ExerciseStatus,
  ExerciseView,
  GradeReport,
  LessonView,
  Me,
  ProjectSummary,
  ProjectView,
  MentorAsk,
  MentorState,
  ProgramRun,
  ProgressView,
  Submission,
} from "./types";

export class NotFoundError extends Error {}

/** The session has ended or the learner isn't logged in. */
export class UnauthorisedError extends Error {}

const CSRF_COOKIE = "XSRF-TOKEN";

function readCookie(name: string): string | null {
  const match = document.cookie.split("; ").find((c) => c.startsWith(`${name}=`));
  return match ? decodeURIComponent(match.slice(name.length + 1)) : null;
}

/** Spring Security issues the CSRF cookie lazily; ask for it before the first state-changing request. */
async function csrfToken(): Promise<string> {
  let token = readCookie(CSRF_COOKIE);
  if (!token) {
    await fetch("/api/auth/csrf");
    token = readCookie(CSRF_COOKIE);
  }
  return token ?? "";
}

async function request<T>(path: string, init?: { method: "POST"; body?: unknown }): Promise<T> {
  const headers: Record<string, string> = {};
  if (init) {
    headers["X-XSRF-TOKEN"] = await csrfToken();
    if (init.body !== undefined) {
      headers["Content-Type"] = "application/json";
    }
  }
  const response = await fetch(path, {
    method: init?.method ?? "GET",
    headers,
    body: init?.body === undefined ? undefined : JSON.stringify(init.body),
  });
  if (response.status === 404) {
    throw new NotFoundError(path);
  }
  if (response.status === 401 && !path.startsWith("/api/auth/")) {
    throw new UnauthorisedError("Your session has ended. Log in again to continue.");
  }
  if (!response.ok) {
    let detail = "";
    try {
      detail = (await response.json()).error ?? "";
    } catch {
      // The body wasn't JSON; the status is all we have.
    }
    throw new Error(detail || `Something went wrong (${response.status}). Try again.`);
  }
  if (response.status === 204 || response.headers.get("Content-Length") === "0") {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}

export const api = {
  me: () => request<Me>("/api/auth/me"),
  register: (email: string, displayName: string, password: string) =>
    request<Me>("/api/auth/register", { method: "POST", body: { email, displayName, password } }),
  login: (email: string, password: string) => request<Me>("/api/auth/login", { method: "POST", body: { email, password } }),
  logout: () => request<void>("/api/auth/logout", { method: "POST" }),
  onboard: (experience: string, weeklyHours: number, goal: string) =>
    request<Me>("/api/onboarding", { method: "POST", body: { experience, weeklyHours, goal } }),

  curriculum: () => request<CurriculumView>("/api/curriculum"),
  lesson: (id: string) => request<LessonView>(`/api/lessons/${encodeURIComponent(id)}`),
  visitLesson: (id: string) => request<void>(`/api/lessons/${encodeURIComponent(id)}/visit`, { method: "POST" }),
  exercise: (id: string) => request<ExerciseView>(`/api/exercises/${encodeURIComponent(id)}`),
  attempt: (id: string, submission: Submission, context: AttemptContext = "practice") =>
    request<GradeReport>(`/api/exercises/${encodeURIComponent(id)}/attempts?context=${context}`, {
      method: "POST",
      body: submission,
    }),
  run: (files: Record<string, string>, stdin = "") =>
    request<ProgramRun>("/api/run", { method: "POST", body: { files, stdin } }),

  mentor: (exerciseId: string) => request<MentorState>(`/api/mentor/${encodeURIComponent(exerciseId)}`),
  mentorAsk: (exerciseId: string, ask: MentorAsk) =>
    request<MentorState>(`/api/mentor/${encodeURIComponent(exerciseId)}/ask`, { method: "POST", body: ask }),
  mentorFollowUp: (exerciseId: string) =>
    request<MentorState>(`/api/mentor/${encodeURIComponent(exerciseId)}/follow-up`, { method: "POST" }),
  mentorAnswer: (exerciseId: string, answer: string) =>
    request<MentorState>(`/api/mentor/${encodeURIComponent(exerciseId)}/follow-up/answer`, { method: "POST", body: { answer } }),

  projects: () => request<ProjectSummary[]>("/api/projects"),
  project: (id: string) => request<ProjectView>(`/api/projects/${encodeURIComponent(id)}`),
  projectAttempt: (id: string, milestoneId: string, submission: Submission) =>
    request<GradeReport>(`/api/projects/${encodeURIComponent(id)}/milestones/${encodeURIComponent(milestoneId)}/attempts`, {
      method: "POST",
      body: submission,
    }),
  projectProgress: (id: string) =>
    request<Record<string, ExerciseStatus>>(`/api/progress/projects/${encodeURIComponent(id)}`),

  progress: () => request<ProgressView>("/api/progress"),
  lessonProgress: (id: string) =>
    request<Record<string, ExerciseStatus>>(`/api/progress/lessons/${encodeURIComponent(id)}`),
};
