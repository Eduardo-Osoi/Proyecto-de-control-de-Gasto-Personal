<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const error = ref('')
const cargando = ref(false)
const router = useRouter()
const auth = useAuthStore()

async function entrar() {
  error.value = ''
  cargando.value = true
  try {
    const { data } = await api.post('/auth/login', { email: email.value, password: password.value })
    auth.setSesion(data.access_token)
    const perfil = await api.get('/auth/me')
    auth.setUsuario(perfil.data)
    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'No se pudo iniciar sesión'
  } finally {
    cargando.value = false
  }
}
</script>

<template>
  <div class="contenedor-auth">
    <h1>GastoClaro</h1>
    <p>Entra para ver tus gastos del mes.</p>
    <form class="grid-form" @submit.prevent="entrar">
      <input v-model="email" type="email" placeholder="Correo" required autocomplete="email" />
      <input v-model="password" type="password" placeholder="Contraseña" required autocomplete="current-password" />
      <p v-if="error" class="error">{{ error }}</p>
      <button class="boton" type="submit" :disabled="cargando">
        {{ cargando ? 'Entrando…' : 'Entrar' }}
      </button>
    </form>
    <p>¿No tienes cuenta? <router-link to="/registro">Regístrate</router-link></p>
  </div>
</template>
