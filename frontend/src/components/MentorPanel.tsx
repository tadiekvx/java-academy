import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "../api";
import type { MentorAsk, MentorMessage, MentorState } from "../types";
import { JavaCode } from "./JavaCode";
import { PlainMarkdown } from "./Markdown";

interface Props {
  exerciseId: string;
  /** The learner's current code, sent so the mentor can see what they're working on. */
  code?: string;
  /** Changes whenever an attempt is recorded, so unlock conditions are re-read. */
  attemptCount: number;
}

/**
 * The AI mentor for one exercise. The server decides how much help is allowed
 * (docs/curriculum/04-ai-mentor-policy.md); this panel shows the conversation and what unlocks next.
 */
export function MentorPanel({ exerciseId, code, attemptCount }: Props) {
  const [open, setOpen] = useState(false);
  const [state, setState] = useState<MentorState | null>(null);
  const [question, setQuestion] = useState("");
  const [hypothesis, setHypothesis] = useState("");
  const [answer, setAnswer] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [confirming, setConfirming] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  const load = useCallback(() => {
    api.mentor(exerciseId).then(setState).catch((e) => setError(e instanceof Error ? e.message : String(e)));
  }, [exerciseId]);

  useEffect(() => {
    if (open) {
      load();
    }
  }, [open, load, attemptCount]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ block: "nearest" });
  }, [state?.thread.length]);

  const run = async (action: () => Promise<MentorState>) => {
    setBusy(true);
    setError(null);
    try {
      setState(await action());
      return true;
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      return false;
    } finally {
      setBusy(false);
    }
  };

  const ask = async (request: MentorAsk) => {
    const ok = await run(() => api.mentorAsk(exerciseId, { ...request, code }));
    if (ok) {
      setQuestion("");
      setConfirming(false);
    }
  };

  if (!open) {
    return (
      <div className="mentor-toggle">
        <button type="button" className="button subtle" onClick={() => setOpen(true)}>
          💬 Ask the mentor
        </button>
      </div>
    );
  }

  const next = state?.next;
  const needsHypothesis = !!state?.attemptFirst && !!next && next.level.code !== "H1";

  return (
    <section className="mentor" aria-label="Mentor">
      <header className="mentor-header">
        <h4>Mentor</h4>
        {state?.current && (
          <span className="mentor-level" title={state.current.description}>
            Help so far: {state.current.code} {state.current.name}
          </span>
        )}
        <button type="button" className="link-button small" onClick={() => setOpen(false)}>
          Hide
        </button>
      </header>

      {!state ? (
        <p className="muted small">Loading…</p>
      ) : !state.available ? (
        <p className="muted small">The mentor isn't set up on this server yet.</p>
      ) : (
        <>
          {state.thread.length === 0 && (
            <p className="muted small">
              Ask about anything in this exercise. The mentor won't hand you the answer. It helps you find it, a little more
              each time you ask for more help.
            </p>
          )}
          <ol className="mentor-thread">
            {state.thread.map((m, i) => (
              <MentorBubble key={i} message={m} />
            ))}
          </ol>
          <div ref={endRef} />
          {busy && <p className="mentor-thinking" role="status">The mentor is thinking…</p>}
          {state.notice && <p className="notice review">{state.notice}</p>}
          {error && <p className="notice error">{error}</p>}

          {state.followUpAvailable && !state.followUpPending && (
            <div className="mentor-followup">
              <p>You solved this with some help. One quick question from the mentor will check the idea has stuck.</p>
              <button type="button" className="button" disabled={busy} onClick={() => run(() => api.mentorFollowUp(exerciseId))}>
                Answer a question
              </button>
            </div>
          )}

          {state.followUpPending ? (
            <form
              className="mentor-form"
              onSubmit={(e) => {
                e.preventDefault();
                run(() => api.mentorAnswer(exerciseId, answer)).then((ok) => ok && setAnswer(""));
              }}
            >
              <label className="field-label" htmlFor={`${exerciseId}-followup`}>
                Your answer
              </label>
              <textarea id={`${exerciseId}-followup`} rows={3} value={answer} onChange={(e) => setAnswer(e.target.value)} />
              <button type="submit" className="button primary" disabled={busy || answer.trim() === ""}>
                Send answer
              </button>
            </form>
          ) : (
            <form
              className="mentor-form"
              onSubmit={(e) => {
                e.preventDefault();
                ask({ text: question });
              }}
            >
              <label className="visually-hidden" htmlFor={`${exerciseId}-question`}>
                Your question
              </label>
              <textarea
                id={`${exerciseId}-question`}
                rows={2}
                placeholder="Ask a question about this exercise…"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
              <div className="button-row">
                <button type="submit" className="button primary" disabled={busy || question.trim() === ""}>
                  Ask
                </button>
              </div>
            </form>
          )}

          {next && !state.followUpPending && (
            <div className="mentor-next">
              {state.attemptFirst && (
                <p className="small">
                  Let's slow down and try things first: the mentor will give smaller hints for a while. That's what
                  makes the ideas stick.
                </p>
              )}
              {needsHypothesis && (
                <>
                  <label className="field-label" htmlFor={`${exerciseId}-hypothesis`}>
                    In one sentence: what do you think is going wrong?
                  </label>
                  <input
                    id={`${exerciseId}-hypothesis`}
                    className="text-input"
                    value={hypothesis}
                    onChange={(e) => setHypothesis(e.target.value)}
                  />
                </>
              )}
              {confirming ? (
                <div className="mentor-confirm" role="alertdialog" aria-label="Confirm walkthrough">
                  <p>{next.reason}</p>
                  <div className="button-row">
                    <button
                      type="button"
                      className="button primary"
                      disabled={busy}
                      onClick={() => ask({ escalate: true, confirmWalkthrough: true, hypothesis })}
                    >
                      Show me the walkthrough
                    </button>
                    <button type="button" className="button" onClick={() => setConfirming(false)}>
                      Keep trying
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <button
                    type="button"
                    className="button"
                    disabled={busy || !next.allowed || (needsHypothesis && hypothesis.trim() === "")}
                    onClick={() => (next.needsConfirmation ? setConfirming(true) : ask({ escalate: true, hypothesis }))}
                  >
                    More help: {next.level.name}
                  </button>
                  <span className="muted small"> {next.level.description}</span>
                  {!next.allowed && next.reason && <p className="mentor-locked small">🔒 {next.reason}</p>}
                </>
              )}
            </div>
          )}
          <p className="muted tiny">
            {state.remainingToday} mentor requests left today · Help up to {state.cap.code} {state.cap.name} here
          </p>
        </>
      )}
    </section>
  );
}

function MentorBubble({ message }: { message: MentorMessage }) {
  if (message.role === "learner") {
    return (
      <li className="mentor-bubble learner">
        <p>{message.content}</p>
      </li>
    );
  }
  return (
    <li className="mentor-bubble mentor-said">
      <span className="mentor-bubble-level">
        {message.kind === "follow_up_question"
          ? "Quick check"
          : message.kind === "follow_up_feedback"
            ? `Feedback · ${message.score}/2`
            : message.level}
      </span>
      <PlainMarkdown text={message.content} />
      {message.code && (
        <>
          <p className="muted tiny">Checked before showing: this code compiles and runs.</p>
          <JavaCode code={message.code} />
        </>
      )}
    </li>
  );
}
