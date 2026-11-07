import { useEffect, useState, type ReactNode } from "react";
import { Link, NavLink, useLocation, useNavigate } from "react-router";
import javaLogo from "../assets/java-logo.png";
import { BookOpen, Brain, FolderKanban, House, LogOut, Menu, Moon, Sparkles, Sun, X } from "lucide-react";
import { api } from "../api";
import { useAuth } from "../auth";
import { moduleHue } from "../look";
import { currentTheme, onThemeChange, setTheme, type Theme } from "../theme";
import type { CurriculumView } from "../types";

/** The app shell: TailAdmin-style sidebar and sticky header around the page content. */
export function Layout({ children }: { children: ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  useEffect(() => setSidebarOpen(false), [location.pathname]);

  return (
    <div className="app">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <Sidebar open={sidebarOpen} />
      <div className={sidebarOpen ? "sidebar-backdrop open" : "sidebar-backdrop"} onClick={() => setSidebarOpen(false)} />
      <div className="app-main">
        <Topbar sidebarOpen={sidebarOpen} onToggleSidebar={() => setSidebarOpen((open) => !open)} />
        <main id="main" className={pageClass(location.pathname)}>
          {children}
        </main>
        <footer className="site-footer">
          Development build. Code runs on this computer with the local runner, which is not a sandbox.
        </footer>
      </div>
    </div>
  );
}

function Sidebar({ open }: { open: boolean }) {
  const { learner } = useAuth();
  const location = useLocation();
  const [curriculum, setCurriculum] = useState<CurriculumView | null>(null);
  const [dueChecks, setDueChecks] = useState(0);

  useEffect(() => {
    api.curriculum().then(setCurriculum).catch(() => setCurriculum(null));
  }, []);

  useEffect(() => {
    if (learner) {
      api.progress().then((p) => setDueChecks(p.dueChecks.length)).catch(() => setDueChecks(0));
    }
  }, [learner, location.pathname]);

  return (
    <aside className={open ? "sidebar open" : "sidebar"} aria-label="Main navigation">
      <Link to="/" className="sidebar-brand">
        <img className="brand-mark" src={javaLogo} alt="" width={36} height={36} />
        Java Academy
      </Link>

      <nav className="sidebar-group" aria-label="Menu">
        <p className="sidebar-group-label">Menu</p>
        <ul className="menu">
          <li>
            <NavLink to="/" end className={({ isActive }) => (isActive ? "menu-item active" : "menu-item")}>
              <House size={20} aria-hidden="true" />
              {learner ? "Dashboard" : "Home"}
            </NavLink>
          </li>
          <li>
            <NavLink to="/lessons" end className={({ isActive }) => (isActive ? "menu-item active" : "menu-item")}>
              <BookOpen size={20} aria-hidden="true" />
              All lessons
            </NavLink>
          </li>
          <li>
            <NavLink to="/projects" className={({ isActive }) => (isActive ? "menu-item active" : "menu-item")}>
              <FolderKanban size={20} aria-hidden="true" />
              Projects
            </NavLink>
          </li>
          {learner && (
            <li>
              <Link to="/#checks" className="menu-item">
                <Brain size={20} aria-hidden="true" />
                Knowledge checks
                {dueChecks > 0 && <span className="menu-badge">{dueChecks}</span>}
              </Link>
            </li>
          )}
        </ul>
      </nav>

      {curriculum?.stages.map((stage) => (
        <nav key={stage.number} className="sidebar-group" aria-label={`Stage ${stage.number}`}>
          <p className="sidebar-group-label">
            Stage {stage.number} · {stage.title.replace(/ in Java$/, "")}
          </p>
          <ul className="menu">
            {stage.modules.map((module) => {
              const ready = module.lessons.filter((l) => l.available).length;
              return (
                <li key={module.number} className={moduleHue(module.number)}>
                  <Link to={`/lessons#module-${stage.number}-${module.number}`} className="menu-item">
                    <span className="module-dot" aria-hidden="true" />
                    {module.title}
                    <span className="menu-count">
                      {ready}/{module.lessons.length}
                    </span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      ))}

      <div className="sidebar-widget">
        <strong>
          <Sparkles size={16} aria-hidden="true" /> Stuck on an exercise?
        </strong>
        Every exercise has a mentor. It helps you find the answer yourself, a little more each time you ask.
      </div>
    </aside>
  );
}

function Topbar({ sidebarOpen, onToggleSidebar }: { sidebarOpen: boolean; onToggleSidebar: () => void }) {
  const { learner, logout } = useAuth();
  const navigate = useNavigate();
  const [theme, setThemeState] = useState<Theme>(currentTheme());

  useEffect(() => onThemeChange(setThemeState), []);

  return (
    <header className="topbar">
      <button type="button" className="icon-button menu-toggle" aria-label="Toggle navigation" onClick={onToggleSidebar}>
        {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
      </button>
      <div className="topbar-actions">
        <button
          type="button"
          className="icon-button"
          aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          {theme === "dark" ? <Sun size={19} /> : <Moon size={19} />}
        </button>
        {learner ? (
          <>
            <span className="user-chip">
              <span className="avatar" aria-hidden="true">
                {initials(learner.displayName)}
              </span>
              <span className="user-name">{learner.displayName}</span>
            </span>
            <button
              type="button"
              className="button"
              onClick={async () => {
                await logout();
                navigate("/");
              }}
            >
              <LogOut size={16} aria-hidden="true" /> Log out
            </button>
          </>
        ) : learner === null ? (
          <>
            <Link to="/login" className="button subtle">
              Log in
            </Link>
            <Link to="/signup" className="button primary">
              Sign up free
            </Link>
          </>
        ) : null}
      </div>
    </header>
  );
}

/** Auth pages run edge to edge; reading pages are narrower than dashboards. */
function pageClass(path: string): string {
  if (/^\/(login|signup)/.test(path)) {
    return "page full";
  }
  return /^\/(lessons\/|checks\/|welcome|projects\/)/.test(path) ? "page narrow" : "page";
}

function initials(name: string): string {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]!.toUpperCase())
    .join("");
}
