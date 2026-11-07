import { useEffect, useRef } from "react";
import Editor, { type OnMount } from "@monaco-editor/react";
import { editorTheme, monaco } from "../monaco";
import type { Diagnostic } from "../types";

const LINE_HEIGHT = 20;
const MIN_LINES = 3;
const MAX_LINES = 30;

interface Props {
  value: string;
  onChange?: (value: string) => void;
  readOnly?: boolean;
  diagnostics?: Diagnostic[];
  label: string;
}

/** A Monaco editor for one Java file. Grows with its content and marks compiler diagnostics. */
export function CodeEditor({ value, onChange, readOnly = false, diagnostics = [], label }: Props) {
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);
  const lines = Math.min(MAX_LINES, Math.max(MIN_LINES, value.split("\n").length + 1));

  const handleMount: OnMount = (editor) => {
    editorRef.current = editor;
    showMarkers(editor, diagnostics);
  };

  useEffect(() => {
    if (editorRef.current) {
      showMarkers(editorRef.current, diagnostics);
    }
  }, [diagnostics]);

  return (
    <div className="code-editor" aria-label={label}>
      <Editor
        height={lines * LINE_HEIGHT + 16}
        language="java"
        theme={editorTheme()}
        value={value}
        onChange={(v) => onChange?.(v ?? "")}
        onMount={handleMount}
        options={{
          readOnly,
          minimap: { enabled: false },
          lineHeight: LINE_HEIGHT,
          fontSize: 14,
          tabSize: 4,
          insertSpaces: true,
          scrollBeyondLastLine: false,
          renderLineHighlight: readOnly ? "none" : "line",
          padding: { top: 8, bottom: 8 },
          ariaLabel: label,
          automaticLayout: true,
          scrollbar: { alwaysConsumeMouseWheel: false },
        }}
      />
    </div>
  );
}

function showMarkers(editor: monaco.editor.IStandaloneCodeEditor, diagnostics: Diagnostic[]) {
  const model = editor.getModel();
  if (!model) {
    return;
  }
  const markers = diagnostics
    .filter((d) => d.line > 0 && d.line <= model.getLineCount())
    .map((d) => ({
      severity: d.kind === "ERROR" ? monaco.MarkerSeverity.Error : monaco.MarkerSeverity.Warning,
      message: d.message,
      startLineNumber: d.line,
      startColumn: Math.max(1, d.column),
      endLineNumber: d.line,
      endColumn: model.getLineMaxColumn(d.line),
    }));
  monaco.editor.setModelMarkers(model, "javac", markers);
}
