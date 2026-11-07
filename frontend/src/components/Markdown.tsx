import ReactMarkdown, { type Components } from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import { Link } from "react-router";
import { JavaCode } from "./JavaCode";
import { RunnableSnippet } from "./RunnableSnippet";

const LESSON_LINK = /^(?:\/lessons\/)?(j\d+-l[\d.]+)$/;

const components: Components = {
  // Code blocks render their own <pre>; inline code stays a plain <code>.
  pre: ({ children }) => <>{children}</>,
  code: ({ className, children }) => {
    const text = String(children ?? "");
    if (className === "language-java-runnable") {
      return <RunnableSnippet code={text} />;
    }
    if (className === "language-java") {
      return <JavaCode code={text} />;
    }
    if (className || text.includes("\n")) {
      return (
        <pre className="code-block">
          <code>{text}</code>
        </pre>
      );
    }
    return <code>{children}</code>;
  },
  a: ({ href, children }) =>
    href && LESSON_LINK.test(href) ? (
      <Link to={`/lessons/${LESSON_LINK.exec(href)![1]}`}>{children}</Link>
    ) : (
      <a href={href} target="_blank" rel="noreferrer">
        {children}
      </a>
    ),
  table: ({ children }) => (
    <div className="table-scroll">
      <table>{children}</table>
    </div>
  ),
};

/**
 * Renders lesson Markdown. Raw HTML is allowed because lesson content comes only from the
 * reviewed repository, never from learners.
 */
export function Markdown({ text }: { text: string }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]} components={components}>
      {text}
    </ReactMarkdown>
  );
}

/** Markdown for exercise prompts, which need no raw HTML. */
export function PlainMarkdown({ text }: { text: string }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
      {text}
    </ReactMarkdown>
  );
}
