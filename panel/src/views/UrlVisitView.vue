<template>

<section>
    <article class="flex flex-col  gap-4 p-4">
    <fieldset class="fieldset bg-base-200 rounded-box w-full p-4 shadow-xl border border-primary">
        <legend class="fieldset-legend">Url details ({{ url_id }})</legend>
        <div class="gird flex grid-cols-2 h-60">
            <div class="text-lg w-full">
                <div class="mb-2">
                    <button class="btn btn-primary">Edit</button>
                </div>
                <ul>
                    <li><strong>Url:</strong> {{ url_data.url }}</li>
                    <li><strong>Code:</strong> {{ url_data.code }}</li>
                    <li><strong>Created:</strong>  {{ humanReadable(url_data.created_at) }}</li>
                    <li>
                        <strong>Type: </strong>
                        <div class="tooltip tooltip-bottom tooltip-primary" data-tip="Image"><Icon v-if="url_data.url_type === 'image'" :icon="faImage" /></div> 
                        <div class="tooltip tooltip-bottom tooltip-primary" data-tip="Video"><Icon v-if="url_data.url_type === 'video'" :icon="faVideo" /></div> 
                        <div class="tooltip tooltip-bottom tooltip-primary" data-tip="Url"><Icon v-if="url_data.url_type === 'url'" :icon="faLink" /></div>
                    </li>
                </ul>
            </div>
            <div class="rounded shadow bg-base-300 w-1/2 flex justify-center">
                <span v-if="url_data.url_type !== 'image'" class="m-auto">Coming soon</span>
                <div
                v-else
                class="bg-no-repeat bg-center h-full w-full"
                :style="`background-image: url(${url_data.url}); background-size: contain;`">
                </div>
            </div>
        </div>
    </fieldset>

    <hr>

    <fieldset class="fieldset bg-base-200 rounded-box w-full p-4 shadow-xl border border-primary">
        <legend class="fieldset-legend">Visit details ({{ visit_data.length }})</legend>
        <div role="tablist" class="tabs tabs-border">
            <a role="tab" class="tab" :class="tab === 'charts' ? 'tab-active':''" @click="tab='charts'">Chart's</a>
            <a role="tab" class="tab" :class="tab === 'logs' ? 'tab-active':''" @click="tab='logs'">Log's</a>
        </div>
        <div v-if="tab === 'charts'" class="flex flex-col gap-4">
            <div class="flex gap-2">
                <select v-model="selectedYear" class="select select-bordered select-sm">
                <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
                </select>

                <select v-model="selectedMonth" class="select select-bordered select-sm">
                <option value="all">All</option>
                <option v-for="m in 12" :key="m" :value="m">
                    {{ String(m).padStart(2,'0') }}
                </option>
                </select>
            </div>
            <Chart
                type="line"
                height="350"
                :options="chartOptions"
                :series="series"
            />
        </div>
        <div v-if="tab === 'logs'">
            <label class="input w-full border-0 border-b shadow outline-0 my-4">
                <Icon :icon="faSearch" />
                <input class="grow" placeholder="You can search IP | Provider | Countries, | Cities, " type="text">
            </label>
            <div class="overflow-x-auto max-h-80">
                <table class="table table-zebra">
                <thead class="sticky top-0 z-10 bg-base-100">
                    <tr>
                        <th></th>
                        <th class="text-center">Country</th>
                        <th class="text-center">City</th>
                        <th class="text-center">Ip Address</th>
                        <th class="text-center">Count</th>
                        <th class="text-center">Date-Time</th>
                        <th class="text-center">Edit</th>
                        <!-- <th class="text-center">Delete</th> -->
                    </tr>
                </thead>
                <tbody>
                    <template v-for="(visit, index) in visit_data" :key="index">
                    <tr class="text-center" :class="2%index === 0 ? 'bg-base-300': ''">
                        <th>{{ index + 1 }}</th>
                        <td>{{ visit.country ? visit.country:'-' }}</td>
                        <td>{{ visit.city ? visit.city:'-' }}</td>
                        <td>{{ visit.ip_address ? visit.ip_address:'-' }}</td>
                        <td>{{ visit.count }}</td>
                        <td>{{ humanReadable(visit.action_at) }}</td>
                        <td @click="visit.show_detail =! visit.show_detail" class="min-w-32">
                            <span class="">{{ visit.show_detail ? 'Hide':'Details'}}</span>
                        </td>
                    </tr>
                    <tr v-if="visit.show_detail">
                        <td class="shadow" :colspan="7">
                            <ul>
                                <li><strong>Provider: </strong>{{visit.ip_provider}}</li>
                                <li><strong>User Agent: </strong>{{visit.user_agent}}</li>
                            </ul> 
                        </td>
                    </tr>
                    </template>

                </tbody>
                </table>
            </div>
        </div>
    </fieldset>
    </article>
</section>
</template>

<script setup>
import axios from "axios"
import { ref, computed, watch, onMounted, defineProps } from "vue"
import dayjs from "dayjs"
import utc from "dayjs/plugin/utc"
import localizedFormat from "dayjs/plugin/localizedFormat"
import Chart from "vue3-apexcharts"
import { faSearch, faImage, faVideo, faLink } from "@fortawesome/free-solid-svg-icons"

dayjs.extend(utc)
dayjs.extend(localizedFormat)

/* ------------------ PROPS ------------------ */
const { url_id, url_code } = defineProps(["url_id", "url_code"])

/* ------------------ HELPERS ------------------ */
const humanReadable = iso =>
  dayjs.utc(iso).local().format("DD MMMM YYYY HH:mm")

const groupBy = (arr, fn) =>
  arr.reduce((a, c) => {
    const k = fn(c)
    a[k] = (a[k] || 0) + 1
    return a
  }, {})

/* ------------------ STATE ------------------ */
const visit_data = ref([])
const url_data = ref([])
const tab = ref("logs")

/* ------------------ FETCH ------------------ */
const get_url_visit_action_list = async () => {
  const r = await axios.get("/admin/analytical/list", {
    params: { url_id }
  })
  visit_data.value = r.data
  visit_data.value.forEach(v => (v.show_detail = false))
}

const get_url_data = async () => {
  const r = await axios.get("/admin/url", {
    params: { code: url_code }
  })
  url_data.value = r.data
}

/* ------------------ DATES ------------------ */
const dates = computed(() =>
  visit_data.value.map(v => new Date(v.action_at))
)

const years = computed(() =>
  [...new Set(dates.value.map(d => d.getFullYear()))].sort()
)

/* ------------------ AUTO TODAY ------------------ */
const today = new Date()
const selectedYear = ref(today.getFullYear())
const selectedMonth = ref(String(today.getMonth() + 1))
const selectedDay = ref(null)

/* ------------------ CHART ------------------ */
const chartOptions = ref({
  chart: {
    toolbar: { show: false },
    events: {
      dataPointSelection(_, ctx, { dataPointIndex }) {
        const x = ctx.opts.xaxis.categories[dataPointIndex]

        // month → day
        if (selectedMonth.value === "all") {
          selectedMonth.value = Number(x)
          return
        }

        // day → hour
        if (!selectedDay.value) {
          selectedDay.value = Number(x)
        }
      }
    }
  },
  stroke: { curve: "smooth" },
  xaxis: { categories: [] },
  annotations: { xaxis: [] }
})

const series = ref([{ name: "Visits", data: [] }])

/* ------------------ CORE ------------------ */
const updateChart = () => {
  const filtered = dates.value.filter(d =>
    d.getFullYear() === selectedYear.value &&
    (selectedMonth.value === "all" ||
      d.getMonth() + 1 === Number(selectedMonth.value))
  )

  if (!filtered.length && selectedMonth.value !== "all") {
    selectedMonth.value = "all"
    return
  }

  // HOURLY (drill-down)
  if (selectedDay.value) {
    const hourly = filtered.filter(
      d => d.getDate() === selectedDay.value
    )

    const grouped = groupBy(hourly, d =>
      String(d.getHours()).padStart(2, "0")
    )

    const categories = Object.keys(grouped)
      .map(Number)
      .sort((a, b) => a - b)
      .map(h => String(h).padStart(2, "0"))

    chartOptions.value.xaxis.categories = categories
    chartOptions.value.annotations.xaxis = []
    series.value = [{ name: "Visits", data: categories.map(c => grouped[c]) }]
    return
  }

  // DAILY / MONTHLY
  const grouped =
    selectedMonth.value === "all"
      ? groupBy(filtered, d =>
          String(d.getMonth() + 1).padStart(2, "0")
        )
      : groupBy(filtered, d =>
          String(d.getDate()).padStart(2, "0")
        )

  const categories = Object.keys(grouped)
    .map(Number)
    .sort((a, b) => a - b)
    .map(n => String(n).padStart(2, "0"))

  chartOptions.value.xaxis.categories = categories
  series.value = [{ name: "Visits", data: categories.map(c => grouped[c]) }]

  // TODAY LINE
  chartOptions.value.annotations.xaxis = []
  if (selectedMonth.value !== "all") {
    const todayDay = String(today.getDate()).padStart(2, "0")
    if (categories.includes(todayDay)) {
      chartOptions.value.annotations.xaxis.push({
        x: todayDay,
        borderColor: "#ef4444",
        label: {
          text: "Today",
          style: { background: "#ef4444", color: "#fff" }
        }
      })
    }
  }
}

/* ------------------ WATCHERS ------------------ */
watch([visit_data, selectedYear, selectedMonth], updateChart)
watch(selectedMonth, () => (selectedDay.value = null))

/* ------------------ MOUNT ------------------ */
onMounted(async () => {
  await get_url_visit_action_list()
  await get_url_data()
})
</script>
