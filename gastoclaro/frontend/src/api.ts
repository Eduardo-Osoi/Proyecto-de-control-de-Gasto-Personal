import axios from 'axios'
import { useAuthStore } from './stores/auth'
import router from './router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

// si el token ya expiró, mando a login en vez de dejar la pantalla trabada
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const auth = useAuthStore()
      auth.cerrarSesion()
      router.push('/login')
    }
    return Promise.reject(error)
  },
)

export default api
