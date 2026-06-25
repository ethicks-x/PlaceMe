<script setup></script>

<template>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" width="100%" height="100%">
    <defs>
      <!-- Modern Gradient for the Icon -->
      <linearGradient id="brandGradient" x1="0%" y1="100%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#0052D4" />
        <stop offset="50%" stop-color="#4364F7" />
        <stop offset="100%" stop-color="#6FB1FC" />
      </linearGradient>

      <!-- Subtle Shadow Effect -->
      <filter id="dropShadow" x="-10%" y="-10%" width="130%" height="130%">
        <feDropShadow dx="2" dy="5" stdDeviation="4" flood-opacity="0.1" />
      </filter>
    </defs>

    <!-- Group for Logo Icon -->
    <g transform="translate(50, 40)" filter="url(#dropShadow)">
      <!-- Main Graduation Cap (Top Diamond) representing Students -->
      <polygon points="110,30 210,75 110,120 10,75" fill="url(#brandGradient)" />

      <!-- Upward Career Growth Arrow cut-out look (Drawn inside the cap) -->
      <polyline
        points="90,85 110,65 130,85"
        fill="none"
        stroke="#FFFFFF"
        stroke-width="6"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <line
        x1="110"
        y1="65"
        x2="110"
        y2="95"
        stroke="#FFFFFF"
        stroke-width="6"
        stroke-linecap="round"
      />

      <!-- Corporate Tie representing Jobs/Placement -->
      <!-- Tie Knot -->
      <polygon points="95,130 125,130 120,145 100,145" fill="#1e293b" />
      <!-- Tie Body -->
      <polygon points="100,147 120,147 125,200 110,220 95,200" fill="#1e293b" />

      <!-- Cap Neck/Base Structure -->
      <path
        d="M50,95 L50,135 C50,150 70,155 110,155 C150,155 170,155 170,135 L170,95"
        fill="none"
        stroke="url(#brandGradient)"
        stroke-width="10"
        stroke-linecap="round"
      />

      <!-- Tassel -->
      <path
        d="M110,75 L185,100 L185,140"
        fill="none"
        stroke="#6FB1FC"
        stroke-width="4"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <rect x="181" y="140" width="8" height="15" rx="2" fill="#6FB1FC" />
    </g>

    <!-- Typography Group -->
    <g transform="translate(300, 145)">
      <!-- Primary Brand Name -->
      <text
        font-family="Poppins, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        font-size="64"
        font-weight="800"
        fill="#f8fafc"
        letter-spacing="-1"
      >
        Place 
        <tspan fill="url(#brandGradient)">Me</tspan>
      </text>

      <!-- Subtitle / Tagline -->
      <text
        y="42"
        x="4"
        font-family="Poppins, system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        font-size="18"
        font-weight="500"
        fill="#94a3b8"
        letter-spacing="6"
      >
        PLACEMENT PORTAL
      </text>
    </g>
  </svg>
</template>
