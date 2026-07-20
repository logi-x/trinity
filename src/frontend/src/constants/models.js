/**
 * Canonical Claude model presets for Trinity UI pickers.
 *
 * Synced from https://platform.claude.com/docs/en/about-claude/models/overview
 * Last updated: 2026-07-08 (#1521)
 *
 * Aliases are undated and resolve to the latest snapshot; do NOT append date
 * suffixes to a current-gen alias. Append [1m] to a value for the 1M
 * extended-context beta (e.g. 'claude-sonnet-4-6[1m]').
 *
 * Keep backend `PUBLIC_CHANNEL_MODELS` in settings_service.py in sync for
 * public-channel overrides (#894) — there is no shared registry across the
 * Python/Vue boundary yet.
 */

export const PRESET_MODELS = [
  // Claude 5 family (latest generation, native 1M context)
  { value: 'claude-fable-5', label: 'Claude Fable 5', note: 'Most capable — longest tasks (latest)' },
  { value: 'claude-sonnet-5', label: 'Claude Sonnet 5', note: 'Fast + smart, 1M context (latest)' },
  // Current generation
  { value: 'claude-opus-4-8', label: 'Claude Opus 4.8', note: 'Most capable Opus' },
  { value: 'claude-opus-4-7', label: 'Claude Opus 4.7', note: 'Current' },
  { value: 'claude-opus-4-6', label: 'Claude Opus 4.6', note: 'Current' },
  { value: 'claude-sonnet-4-6', label: 'Claude Sonnet 4.6', note: 'Fast + smart' },
  { value: 'claude-haiku-4-5-20251001', label: 'Claude Haiku 4.5', note: 'Fastest, cheapest' },
  // Legacy (still active)
  { value: 'claude-opus-4-5-20251101', label: 'Claude Opus 4.5', note: 'Legacy' },
  { value: 'claude-sonnet-4-5-20250929', label: 'Claude Sonnet 4.5', note: 'Legacy' },
]

/** Option label for plain <select> controls (Settings, etc.). */
export function presetOptionLabel(model) {
  return model.note ? `${model.label} — ${model.note}` : model.label
}
