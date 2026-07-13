import { reactive, readonly } from 'vue'
import axios from 'axios'
import { router } from '../router'

// reactive state object
const state = reactive({
  user: null,
  token: null,
  isAuthenticated: false,
})

async function initAuth() {
  const userFromLocalStorage = localStorage.getItem('user')
  const userFromSessionStorage = sessionStorage.getItem('user')
  const tokenFromSessionStorage = sessionStorage.getItem('token')

  let potentialUser = null
  let potentialToken = null

  // rememberMe -> Yes. User is in localStorage, token is in a cookie.
  if (userFromLocalStorage) {
    potentialUser = JSON.parse(userFromLocalStorage)
    // Token is sent automatically by the browser via cookie.
  }
  // rememberMe -> No. User and token are in sessionStorage.
  else if (userFromSessionStorage && tokenFromSessionStorage) {
    potentialUser = JSON.parse(userFromSessionStorage)
    potentialToken = tokenFromSessionStorage
  }

  if (potentialUser) {
    // Re-validate the session with the backend to ensure the token/cookie isn't stale
    try {
      // This relies on the cookie or the token being set in axios headers below
      if (potentialToken) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${potentialToken}`
      }
      // A simple protected endpoint to verify the token is still valid.
      const response = await axios.get('/api/profile')
      // If the above call succeeds, the session is valid.
      _setAuth(response.data, potentialToken)
    } catch (error) {
      // If it fails, the token is invalid. Log out.
      console.error('Session revalidation failed:', error)
      logout()
    }
  }
}

// Sets the authentication state.
function _setAuth(userData, token) {
  state.user = userData
  state.token = token
  state.isAuthenticated = true
  if (token) {
    // Set token for subsequent requests if it's not in a cookie
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
}

function _landingPathForRole(role) {
  if (role === 'admin') return '/admin'
  if (role === 'company') return '/company/pending'
  return '/dashboard'
}

// Handles the login process.
async function login(credentials) {
  const { data } = await axios.post('/api/auth/login', credentials)

  _setAuth(data.user, data.access_token || null)
  console.log('Login response:', data)

  if (credentials.rememberMe) {
    // Backend sets the cookie, frontend stores user data in localStorage.
    localStorage.setItem('user', JSON.stringify(data.user))
  } else {
    // Store both token and user data in sessionStorage.
    sessionStorage.setItem('user', JSON.stringify(data.user))
    sessionStorage.setItem('token', data.access_token)
  }

  // Redirect to the appropriate dashboard
  router.push(_landingPathForRole(data.user.role))
}

// Handles the signup process.
async function signup(signupData) {
  const { data } = await axios.post('/api/auth/register', signupData)

  _setAuth(data.user, data.access_token)
  console.log('Signup response:', data)

  sessionStorage.setItem('user', JSON.stringify(data.user))
  sessionStorage.setItem('token', data.access_token)

  // Redirect to the appropriate dashboard
  router.push(_landingPathForRole(data.user.role))
}

async function registerCompany(companyData) {
  const { data } = await axios.post('/api/auth/register-company', companyData)

  _setAuth(data.user, data.access_token)

  sessionStorage.setItem('user', JSON.stringify(data.user))
  sessionStorage.setItem('token', data.access_token)

  router.push(_landingPathForRole(data.user.role))
}

// Clears all authentication data from state and storage.
async function logout() {
  // Clear state
  state.user = null
  state.token = null
  state.isAuthenticated = false

  // Clear storage
  localStorage.removeItem('user')
  sessionStorage.removeItem('user')
  sessionStorage.removeItem('token')

  // Clear axios header
  delete axios.defaults.headers.common['Authorization']

  // Tell backend to clear the auth cookie
  try {
    await axios.post('/api/auth/logout')
  } catch (error) {
    console.error('Logout API call failed:', error)
  }

  // Redirect to login page
  if (router.currentRoute.value.name !== 'login') {
    router.push({ name: 'login' })
  }
}

export function useAuth() {
  return {
    // Use readonly to prevent direct state mutation from components
    authState: readonly(state),
    initAuth,
    login,
    signup,
    registerCompany,
    logout,
  }
}
