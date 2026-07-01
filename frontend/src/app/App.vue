<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchMeta } from "../api/metaApi";
import type { MetaResponse } from "../types/meta";

const fallbackMeta: MetaResponse = {
  project_name: "厦门市思明区路网结构与可步行性分析平台",
  study_area: "福建省厦门市思明区",
  data_version: "not-loaded",
  stage: "D8 frontend-backend integration",
};

const meta = ref<MetaResponse>(fallbackMeta);
const isLoading = ref(true);
const errorMessage = ref("");

onMounted(async () => {
  try {
    meta.value = await fetchMeta();
  } catch {
    errorMessage.value = "后端连接失败，请确认 FastAPI 服务是否已启动。";
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <main class="app-shell">
    <header class="app-header">
      <div>
        <p class="eyebrow">GIS Engineering Workbench</p>
        <h1>{{ meta.project_name }}</h1>
      </div>
      <div class="header-meta">
        <span>研究区域：{{ meta.study_area }}</span>
        <span>数据版本：{{ meta.data_version }}</span>
        <span>阶段：{{ meta.stage }}</span>
      </div>
    </header>

    <section class="status-card" :class="{ 'status-card--error': errorMessage }">
      <strong>后端连接：</strong>
      <span v-if="isLoading">正在连接后端 API...</span>
      <span v-else-if="errorMessage">{{ errorMessage }}</span>
      <span v-else>已连接，前端已成功读取 `/api/v1/meta`。</span>
    </section>

    <section class="workbench">
      <aside class="panel panel-left">
        <h2>控制面板</h2>
        <p>指标选择、图层开关、路网筛选将在后续迭代接入。</p>
      </aside>

      <section class="map-placeholder">
        <div>
          <p class="eyebrow">Map Canvas</p>
          <h2>地图区域占位</h2>
          <p>后续接入 MapLibre、天地图/OSM 底图和思明区路网数据。</p>
        </div>
      </section>

      <aside class="panel panel-right">
        <h2>分析面板</h2>
        <p>网格详情、道路详情、排行榜和图表将在后续迭代接入。</p>
      </aside>
    </section>
  </main>
</template>
