<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const nombre = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const cargando = ref(false)
const router = useRouter()

async function registrar() {
  error.value = ''
  cargando.value = true
  try {
    await api.post('/auth/registro', { nombre: nombre.value, email: email.value, password: password.value })
    router.push('/login')
  } catch (e: any) {
    const detalle = e.response?.data?.detail
    error.value = Array.isArray(detalle) ? detalle[0]?.msg : (detalle || 'No se pudo crear la cuenta')
  } finally {
    cargando.value = false
  }
}
</script>

<template>
  <div class="contenedor-auth">
    <h1>Crear cuenta</h1>
    <form class="grid-form" @submit.prevent="registrar">
      <input v-model="nombre" type="text" placeholder="Nombre" required />
      <input v-model="email" type="email" placeholder="Correo" required autocomplete="email" />
      <input v-model="password" type="password" placeholder="Contraseña (mín. 8, con un número)" required autocomplete="new-password" />
      <p v-if="error" class="error">{{ error }}</p>
      <button class="boton" type="submit" :disabled="cargando">
        {{ cargando ? 'Creando…' : 'Crear cuenta' }}
      </button>
    </form>
    <p>¿Ya tienes cuenta? <router-link to="/login">Inicia sesión</router-link></p>
  </div>
</template>
