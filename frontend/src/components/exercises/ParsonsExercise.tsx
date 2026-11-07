import { useState } from "react";
import { useAuth } from "../../auth";
import type { ExerciseView } from "../../types";
import { LoginPrompt } from "../LoginPrompt";
import { Results } from "../Results";
import { useAttempt } from "./useAttempt";

/** Build a program by moving blocks into order. Buttons (not drag-and-drop) keep it keyboard-accessible. */
export function ParsonsExercise({ exercise, onRecorded }: { exercise: ExerciseView; onRecorded?: () => void }) {
  const { learner } = useAuth();
  const [order, setOrder] = useState<number[]>([]);
  const attempt = useAttempt(exercise.id, "practice", onRecorded);
  const text = new Map(exercise.blocks.map((b) => [b.index, b.text]));
  const available = exercise.blocks.filter((b) => !order.includes(b.index));

  const change = (next: number[]) => {
    setOrder(next);
    attempt.clear();
  };
  const move = (position: number, delta: number) => {
    const next = [...order];
    const [item] = next.splice(position, 1);
    next.splice(position + delta, 0, item);
    change(next);
  };

  return (
    <div className="parsons-exercise">
      <div className="parsons-columns">
        <div>
          <h4 className="parsons-heading">Blocks</h4>
          <ul className="parsons-list">
            {available.map((block) => (
              <li key={block.index}>
                <button type="button" className="parsons-block" onClick={() => change([...order, block.index])}>
                  <span className="visually-hidden">Add: </span>
                  <code>{block.text.trim()}</code>
                </button>
              </li>
            ))}
            {available.length === 0 && <li className="muted">All blocks used.</li>}
          </ul>
        </div>
        <div>
          <h4 className="parsons-heading">Your program</h4>
          {order.length === 0 ? (
            <p className="muted">Select blocks on the left to add them here, in order.</p>
          ) : (
            <ol className="parsons-program">
              {order.map((index, position) => (
                <li key={index} className="parsons-line">
                  <code className="parsons-code">{text.get(index)}</code>
                  <span className="parsons-actions">
                    <button type="button" aria-label="Move up" disabled={position === 0} onClick={() => move(position, -1)}>
                      ↑
                    </button>
                    <button
                      type="button"
                      aria-label="Move down"
                      disabled={position === order.length - 1}
                      onClick={() => move(position, 1)}
                    >
                      ↓
                    </button>
                    <button type="button" aria-label="Remove" onClick={() => change(order.filter((_, i) => i !== position))}>
                      ✕
                    </button>
                  </span>
                </li>
              ))}
            </ol>
          )}
        </div>
      </div>
      <p className="muted small">Indentation is already set for you; you only choose the order.</p>
      {learner ? (
        <div className="button-row">
          <button
            type="button"
            className="button primary"
            disabled={order.length === 0 || attempt.busy}
            onClick={() => attempt.submit({ order })}
          >
            {attempt.busy ? "Checking…" : "Check my program"}
          </button>
        </div>
      ) : (
        <LoginPrompt action="check your program" />
      )}
      {attempt.error && <p className="notice error">{attempt.error}</p>}
      {attempt.report && <Results report={attempt.report} />}
    </div>
  );
}
