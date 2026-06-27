<script setup lang="ts">
const projectName = "厦门市思明区路网结构与可步行性分析平台";
const stage = "D6 工程骨架";
const dataVersion = "not-loaded";
</script>

<template>
  <main class="app-shell">
    <header class="app-header">
      <div>
        <p class="eyebrow">GIS Engineering Scaffold</p>
        <h1>{{ projectName }}</h1>
      </div>
      <div class="header-meta">
        <span>阶段：{{ stage }}</span>
        <span>数据版本：{{ dataVersion }}</span>
      </div>
    </header>

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
