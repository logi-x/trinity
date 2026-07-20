/**
 * Agent container resource presets — must match backend VALID_CPU / VALID_MEMORY
 * in services/agent_service/capabilities.py (#1197, RES-001).
 */

export const VALID_MEMORY_OPTIONS = [
  { value: '1g', label: '1 GB' },
  { value: '2g', label: '2 GB' },
  { value: '4g', label: '4 GB' },
  { value: '8g', label: '8 GB' },
  { value: '16g', label: '16 GB' },
  { value: '32g', label: '32 GB' },
]

export const VALID_CPU_OPTIONS = [
  { value: '1', label: '1 Core' },
  { value: '2', label: '2 Cores' },
  { value: '4', label: '4 Cores' },
  { value: '8', label: '8 Cores' },
  { value: '16', label: '16 Cores' },
]
