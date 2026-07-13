<script setup></script>

<template>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 230" width="100%" height="100%">
    <!-- Subtle Shadow Effect to separate it from your dark background -->
    <defs>
      <filter id="logoShadow" x="-10%" y="-10%" width="130%" height="130%">
        <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#020617" flood-opacity="0.6" />
      </filter>
    </defs>

    <g filter="url(#logoShadow)">
      <!-- Main Graduation Cap (Top Diamond) - Using your Primary Sky Blue Accent -->
      <polygon points="110,10 210,55 110,100 10,55" fill="#38BDF8" />

      <!-- Upward Career Growth Arrow cut-out look (Drawn inside the cap in high-contrast Off-White) -->
      <polyline
        points="90,65 110,45 130,65"
        fill="none"
        stroke="#F8FAFC"
        stroke-width="6"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <line
        x1="110"
        y1="45"
        x2="110"
        y2="75"
        stroke="#F8FAFC"
        stroke-width="6"
        stroke-linecap="round"
      />

      <!-- Corporate Tie representing Jobs/Placement -->
      <!-- Tie Knot - Deep Tech Indigo -->
      <polygon points="95,110 125,110 120,125 100,125" fill="#0F172A" />
      <!-- Tie Body - Deep Tech Indigo -->
      <polygon points="100,127 120,127 125,180 110,200 95,180" fill="#0F172A" />

      <!-- Cap Neck/Base Structure - Using the Slate Blue for structure -->
      <path
        d="M50,75 L50,115 C50,130 70,135 110,135 C150,135 170,135 170,115 L170,75"
        fill="none"
        stroke="#1E293B"
        stroke-width="10"
        stroke-linecap="round"
      />

      <!-- Tassel using the Mint Green Success Accent to pop -->
      <path
        d="M110,55 L185,80 L185,120"
        fill="none"
        stroke="#34D399"
        stroke-width="4"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <rect x="181" y="120" width="8" height="15" rx="2" fill="#34D399" />
    </g>
  </svg>
</template>
