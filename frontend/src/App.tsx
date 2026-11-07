import type { ReactElement } from "react";
import { BrowserRouter, Link, Navigate, Route, Routes } from "react-router";
import { AuthProvider, useAuth } from "./auth";
import { Layout } from "./components/Layout";
import { CheckPage } from "./pages/CheckPage";
import { CurriculumPage } from "./pages/CurriculumPage";
import { DashboardPage } from "./pages/DashboardPage";
import { LessonPage } from "./pages/LessonPage";
import { LoginPage } from "./pages/LoginPage";
import { ProjectPage } from "./pages/ProjectPage";
import { ProjectsPage } from "./pages/ProjectsPage";
import { SignUpPage } from "./pages/SignUpPage";
import { WelcomePage } from "./pages/WelcomePage";

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/lessons" element={<CurriculumPage />} />
            <Route path="/lessons/:id" element={<LessonPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/projects/:id" element={<ProjectPage />} />
            <Route path="/signup" element={<SignUpPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/welcome" element={<WelcomePage />} />
            <Route path="/checks/:exerciseId" element={<RequireLearner element={<CheckPage />} />} />
            <Route
              path="*"
              element={
                <p>
                  Page not found. <Link to="/">Go to the home page</Link>
                </p>
              }
            />
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  );
}

/** Visitors see the curriculum; learners who haven't finished onboarding go there; everyone else sees their dashboard. */
function Home() {
  const { learner } = useAuth();
  if (learner === undefined) {
    return <p className="muted">Loading…</p>;
  }
  if (learner === null) {
    return <CurriculumPage />;
  }
  if (!learner.onboarded) {
    return <Navigate to="/welcome" replace />;
  }
  return <DashboardPage />;
}

function RequireLearner({ element }: { element: ReactElement }) {
  const { learner } = useAuth();
  if (learner === undefined) {
    return <p className="muted">Loading…</p>;
  }
  return learner ? element : <Navigate to={`/login?next=${encodeURIComponent(window.location.pathname)}`} replace />;
}
