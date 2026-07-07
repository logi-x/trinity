<template>
  <div class="fixed inset-0 z-40 flex justify-end">
    <div class="absolute inset-0 bg-black/30" @click="$emit('close')"></div>

    <div class="relative z-50 w-full max-w-md h-full bg-white dark:bg-gray-900 shadow-xl flex flex-col">
      <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <div class="min-w-0">
          <div class="font-medium text-gray-900 dark:text-white truncate">Files from {{ agent.name }}</div>
          <div class="text-xs text-gray-400">Shared documents you can download</div>
        </div>
        <button class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl leading-none" @click="$emit('close')" aria-label="Close">×</button>
      </div>

      <div class="flex-1 overflow-y-auto p-4">
        <div v-if="loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-7 w-7 border-b-2 border-action-primary-500 mx-auto"></div>
        </div>

        <div v-else-if="error" class="text-sm text-status-danger-600 dark:text-status-danger-400">{{ error }}</div>

        <div v-else-if="docs.length === 0" class="text-center py-12 text-sm text-gray-400">
          <div class="text-3xl mb-2">📄</div>
          No files shared with you yet.
        </div>

        <ul v-else class="space-y-2">
          <li
            v-for="d in docs"
            :key="d.id"
            class="flex items-center gap-3 rounded-lg border border-gray-200 dark:border-gray-800 p-3"
          >
            <span class="text-xl shrink-0">{{ icon(d) }}</span>
            <div class="min-w-0 flex-1">
              <div class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ d.filename }}</div>
              <div class="text-xs text-gray-400">{{ humanSize(d.size_bytes) }}<span v-if="d.created_at"> · {{ formatDate(d.created_at) }}</span></div>
            </div>
            <a
              :href="d.download_url"
              target="_blank"
              rel="noopener"
              class="shrink-0 text-xs px-2.5 py-1 rounded-md bg-action-primary-600 hover:bg-action-primary-700 text-white"
            >Download</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useClientPortalStore } from '@/stores/clientPortal'

const props = defineProps({
  agent: { type: Object, required: true },   // { name }
})
defineEmits(['close'])

const store = useClientPortalStore()
const docs = ref([])
const loading = ref(true)
const error = ref(null)

function humanSize(n) {
  n = Number(n) || 0
  if (n < 1024) return `${n} B`
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`
  return `${(n / 1024 / 1024).toFixed(1)} MB`
}
function icon(d) {
  const t = (d.mime_type || '').toLowerCase()
  if (t.startsWith('image/')) return '🖼️'
  if (t.includes('pdf')) return '📕'
  if (t.includes('zip') || t.includes('tar')) return '🗜️'
  if (t.startsWith('text/') || t.includes('json') || t.includes('csv')) return '📃'
  return '📄'
}
function formatDate(iso) {
  try { return new Date(iso).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }) }
  catch { return iso }
}

onMounted(async () => {
  try {
    docs.value = await store.fetchDocuments(props.agent.name)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load files.'
  } finally {
    loading.value = false
  }
})
</script>
