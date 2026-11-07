import { useEffect, useState } from "react";
import { monaco } from "../monaco";

/** Read-only, syntax-highlighted Java. Shows plain text until highlighting is ready. */
export function JavaCode({ code }: { code: string }) {
  const [html, setHtml] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    monaco.editor
      .colorize(code.replace(/\n$/, ""), "java", { tabSize: 4 })
      .then((result) => {
        if (!cancelled) {
          setHtml(result);
        }
      })
      .catch(() => setHtml(null));
    return () => {
      cancelled = true;
    };
  }, [code]);

  return html === null ? (
    <pre className="code-block">
      <code>{code}</code>
    </pre>
  ) : (
    <pre className="code-block monaco-colorized" dangerouslySetInnerHTML={{ __html: html }} />
  );
}
