<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuth } from './store/auth'

const { authState } = useAuth()
</script>

<template>
  <NavBar :role="authState.user?.role || 'guest'" />
  <main>
    <RouterView />
  </main>
</template>

<style>
:root {
  --background-start: #1e293b;
  --background-middle: #0f172a;
  --background-end: #020617;
  --form-bg: rgba(30, 41, 59, 0.65);
  --text-color: #f8fafc;
  --text-color-muted: #94a3b8;
  --input-bg: rgba(15, 23, 42, 0.6);
  --input-border: rgba(255, 255, 255, 0.1);
  --button-bg-start: #38bdf8;
  --button-bg-end: #34d399;
  --highlight-color: #38bdf8;
}

html,
body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

body {
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(
    135deg,
    var(--background-start) 0%,
    var(--background-middle) 50%,
    var(--background-end) 100%
  );
  min-height: 100vh;
  color: var(--text-color);
  color-scheme: dark;
}
</style>
