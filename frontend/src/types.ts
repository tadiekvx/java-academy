// Mirrors of the backend's API records (academy.api, academy.assessment, academy.execution).

export type LessonStatus = "DRAFT" | "IN_REVIEW" | "PUBLISHED" | "RETIRED";

export interface CurriculumView {
  stages: { number: number; title: string; optional?: boolean; modules: ModuleView[] }[];
}

export interface ModuleView {
  number: number;
  title: string;
  lessons: LessonSummary[];
}

export interface LessonSummary {
  id: string;
  title: string;
  available: boolean;
  status: LessonStatus | null;
}

export interface Objective {
  id: string;
  text: string;
}

export interface ResourceView {
  id: string;
  title: string;
  creator: string;
  url: string;
  kind: string;
  level: "introductory" | "supplementary" | "advanced";
  topic: string;
  why: string;
  embedUrl: string | null;
  published: string | null;
  caveat: string | null;
}

export interface LessonView {
  id: string;
  title: string;
  objectives: Objective[];
  estimatedMinutes: number;
  status: LessonStatus;
  body: string;
  resources: ResourceView[];
}

export type ExerciseType = "PREDICT" | "PARSONS" | "WRITE" | "DEBUG" | "MODIFY" | "EXPLAIN";

export interface ExerciseView {
  id: string;
  type: ExerciseType;
  title: string;
  prompt: string;
  files: Record<string, string>;
  signatures: string[];
  visibleTests: { name: string | null; call: string; expected: string }[];
  blocks: { index: number; text: string }[];
  relatedCode: string | null;
}

export interface Diagnostic {
  file: string | null;
  line: number;
  column: number;
  kind: "ERROR" | "WARNING";
  message: string;
}

export interface RunResult {
  exitCode: number;
  stdout: string;
  stderr: string;
  timedOut: boolean;
  outputLimitExceeded: boolean;
}

export interface ProgramRun {
  diagnostics: Diagnostic[];
  result: RunResult | null;
}

export type TestStatus = "PASS" | "FAIL" | "ERROR" | "TIMEOUT" | "NOT_RUN";

export interface TestResult {
  name: string | null;
  visible: boolean;
  status: TestStatus;
  call: string | null;
  expected: string | null;
  actual: string | null;
  output: string | null;
  error: string | null;
}

export type Outcome = "PASSED" | "FAILED" | "COMPILE_ERROR" | "PENDING_REVIEW";

export interface GradeReport {
  outcome: Outcome;
  message: string;
  diagnostics: Diagnostic[];
  tests: TestResult[];
  actualOutput: string | null;
}

export interface Submission {
  files?: Record<string, string>;
  prediction?: string;
  order?: number[];
  explanation?: string;
}

export interface LearnerView {
  id: number;
  email: string;
  displayName: string;
  onboarded: boolean;
}

export interface Me {
  learner: LearnerView | null;
}

export type Evidence = "IMPL" | "EXPL" | "MIST" | "DEBUG" | "MOD" | "XFER" | "TRADE";
export type Coverage = "INDEPENDENT" | "ASSISTED" | "PENDING_REVIEW" | "MISSING";

export interface ConceptView {
  id: string;
  name: string;
  level: number;
  levelName: string;
  independentExercises: number;
  assistedOnlyExercises: number;
  evidence: { type: Evidence; label: string; coverage: Coverage }[];
  nextCheckDue: string | null;
}

export interface DueCheck {
  exerciseId: string;
  title: string;
  conceptNames: string[];
  dueSince: string;
}

export interface ProgressView {
  concepts: ConceptView[];
  dueChecks: DueCheck[];
  recommended: { id: string; title: string } | null;
}

export interface ExerciseStatus {
  attempts: number;
  passed: boolean;
  passedIndependently: boolean;
  pendingReview: boolean;
}

export type AttemptContext = "practice" | "retrieval";

export interface MentorLevelView {
  code: string;
  name: string;
  description: string;
}

export interface MentorMessage {
  role: "learner" | "mentor";
  kind: "question" | "help" | "follow_up_question" | "follow_up_answer" | "follow_up_feedback";
  level: string;
  content: string;
  code: string | null;
  score: number | null;
  at: string;
}

export interface MentorState {
  available: boolean;
  cap: MentorLevelView;
  current: MentorLevelView | null;
  next: { level: MentorLevelView; allowed: boolean; needsConfirmation: boolean; reason: string | null } | null;
  attemptFirst: boolean;
  followUpAvailable: boolean;
  followUpPending: boolean;
  remainingToday: number;
  notice: string | null;
  thread: MentorMessage[];
}

export interface MentorAsk {
  text?: string;
  escalate?: boolean;
  confirmWalkthrough?: boolean;
  hypothesis?: string;
  code?: string;
}

export interface ProjectSummary {
  id: string;
  title: string;
  category: "A" | "B" | "C";
  summary: string;
  estimatedHours: number | null;
  milestones: number;
  status: LessonStatus;
}

export interface MilestoneView {
  id: string;
  title: string;
  instructions: string;
  signatures: string[];
  visibleTests: { name: string | null; call: string; expected: string }[];
}

export interface ProjectView {
  id: string;
  title: string;
  category: "A" | "B" | "C";
  status: LessonStatus;
  summary: string;
  brief: string;
  estimatedHours: number | null;
  prerequisites: string[];
  requirements: string[];
  constraints: string[];
  acceptance: string[];
  milestones: MilestoneView[];
  rubric: { criterion: string; zero: string; one: string; two: string }[];
  designNotePrompt: string | null;
  files: Record<string, string>;
}
