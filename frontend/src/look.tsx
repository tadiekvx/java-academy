import { Bug, Code, Eye, Layers, ListOrdered, MessageSquare, Pencil, Repeat, Shuffle, Terminal, Wrench, type LucideIcon } from "lucide-react";
import type { ExerciseType } from "./types";

// Colours and icons that give each module and exercise type a consistent identity.

const MODULE_HUES = ["blue", "purple", "orange", "green", "pink", "teal"] as const;
const MODULE_ICONS: LucideIcon[] = [Terminal, Layers, Shuffle, Repeat, Wrench, ListOrdered];

export function moduleHue(moduleNumber: number): string {
  return `hue-${MODULE_HUES[(((moduleNumber - 1) % MODULE_HUES.length) + MODULE_HUES.length) % MODULE_HUES.length]}`;
}

export function ModuleIcon({ moduleNumber, size = 22 }: { moduleNumber: number; size?: number }) {
  const Icon = MODULE_ICONS[(((moduleNumber - 1) % MODULE_ICONS.length) + MODULE_ICONS.length) % MODULE_ICONS.length];
  return <Icon size={size} aria-hidden="true" />;
}

export const EXERCISE_LOOK: Record<ExerciseType, { label: string; hue: string; icon: LucideIcon }> = {
  PREDICT: { label: "Predict, then run", hue: "hue-orange", icon: Eye },
  PARSONS: { label: "Arrange the blocks", hue: "hue-teal", icon: Shuffle },
  WRITE: { label: "Write code", hue: "hue-blue", icon: Code },
  DEBUG: { label: "Fix the bug", hue: "hue-red", icon: Bug },
  MODIFY: { label: "Change working code", hue: "hue-purple", icon: Pencil },
  EXPLAIN: { label: "Explain", hue: "hue-green", icon: MessageSquare },
};
