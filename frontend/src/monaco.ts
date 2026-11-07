import * as monaco from "monaco-editor";
import EditorWorker from "monaco-editor/editor/editor.worker?worker";
import { loader } from "@monaco-editor/react";
import { currentTheme, onThemeChange } from "./theme";

// Bundle Monaco locally instead of letting @monaco-editor/react fetch it from a CDN.
self.MonacoEnvironment = { getWorker: () => new EditorWorker() };
loader.config({ monaco });

export function editorTheme(): string {
  return currentTheme() === "dark" ? "vs-dark" : "vs";
}

monaco.editor.setTheme(editorTheme());
onThemeChange(() => monaco.editor.setTheme(editorTheme()));

export { monaco };
