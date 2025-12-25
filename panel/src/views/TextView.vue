<template>
  <div style="display:flex; gap:12px; margin-bottom:12px;">
    <select v-model="selectedYear">
      <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
    </select>

    <select v-model="selectedMonth">
      <option value="all">All</option>
      <option v-for="m in 12" :key="m" :value="m">
        {{ String(m).padStart(2, '0') }}
      </option>
    </select>
  </div>

  <Chart
    type="line"
    height="350"
    :options="chartOptions"
    :series="series"
  />
</template>

<script setup>
import { ref, watch } from "vue"

/* ------------------ FAKE ORDER DATA ------------------ */
const rawData = [
  { action_at: "2023-02-22T10:15:06+00:00" },
  { action_at: "2023-02-25T14:30:12+00:00" },

  { action_at: "2024-02-22T09:05:06+00:00" },

  { action_at: "2025-02-22T08:10:06+00:00" },
  { action_at: "2025-02-25T04:30:07+00:00" },

  { action_at: "2025-12-25T07:15:07+00:00" },
  { action_at: "2025-12-25T11:15:51+00:00" }
]

const dates = rawData.map(i => new Date(i.action_at))

const years = [...new Set(dates.map(d => d.getFullYear()))].sort()

const today = new Date()

const selectedYear = ref(today.getFullYear())
const selectedMonth = ref(String(today.getMonth() + 1))

const chartOptions = ref({
  chart: {
    toolbar: { show: false }
  },
  stroke: { curve: "smooth" },
  xaxis: { categories: [] }
})

const series = ref([{ name: "Orders", data: [] }])

const groupBy = (arr, keyFn) =>
  arr.reduce((acc, item) => {
    const k = keyFn(item)
    acc[k] = (acc[k] || 0) + 1
    return acc
  }, {})

const updateChart = () => {
  const filtered = dates.filter(d =>
    d.getFullYear() === selectedYear.value &&
    (selectedMonth.value === "all" ||
      d.getMonth() + 1 === Number(selectedMonth.value))
  )

  // AUTO TODAY FALLBACK
  if (!filtered.length && selectedMonth.value !== "all") {
    selectedMonth.value = "all"
    return
  }

  let grouped

  if (selectedMonth.value === "all") {
    // MONTHLY
    grouped = groupBy(filtered, d =>
      String(d.getMonth() + 1).padStart(2, "0")
    )
  } else {
    // DAILY
    grouped = groupBy(filtered, d =>
      String(d.getDate()).padStart(2, "0")
    )
  }

  const categories = Object.keys(grouped)
    .map(Number)
    .sort((a, b) => a - b)
    .map(n => String(n).padStart(2, "0"))

  series.value = [
    {
      name: "Orders",
      data: categories.map(c => grouped[c])
    }
  ]

  chartOptions.value.xaxis.categories = categories
}
watch([selectedYear, selectedMonth], updateChart, { immediate: true })
</script>
