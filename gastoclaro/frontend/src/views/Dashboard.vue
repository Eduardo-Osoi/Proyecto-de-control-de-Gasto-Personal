<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'

interface Categoria { id: number; nombre: string; presupuesto_mensual: number }
interface Gasto { id: number; descripcion: string; monto: number; fecha: string; categoria_id: number }

const auth = useAuthStore()
const router = useRouter()

const categorias = ref<Categoria[]>([])
const gastos = ref<Gasto[]>([])
const error = ref('')
const cargandoInicial = ref(true)

const nuevaCategoria = ref('')
const presupuestoCategoria = ref<number | null>(null)

const descripcionGasto = ref('')
const montoGasto = ref<number | null>(null)
const categoriaGasto = ref<number | null>(null)

const totalMes = computed(() => gastos.value.reduce((acc, g) => acc + g.monto, 0))

function nombreCategoria(id: number) {
  return categorias.value.find((c) => c.id === id)?.nombre || '—'
}

async function cargarTodo() {
  try {
    const [cats, gts] = await Promise.all([api.get('/categorias/'), api.get('/gastos/')])
    categorias.value = cats.data
    gastos.value = gts.data
  } catch {
    error.value = 'No se pudo cargar la información'
  } finally {
    cargandoInicial.value = false
  }
}

async function crearCategoria() {
  if (!nuevaCategoria.value.trim()) return
  await api.post('/categorias/', {
    nombre: nuevaCategoria.value,
    presupuesto_mensual: presupuestoCategoria.value || 0,
  })
  nuevaCategoria.value = ''
  presupuestoCategoria.value = null
  await cargarTodo()
}

async function crearGasto() {
  if (!descripcionGasto.value.trim() || !montoGasto.value || !categoriaGasto.value) return
  await api.post('/gastos/', {
    descripcion: descripcionGasto.value,
    monto: montoGasto.value,
    categoria_id: categoriaGasto.value,
  })
  descripcionGasto.value = ''
  montoGasto.value = null
  await cargarTodo()
}

async function eliminarGasto(id: number) {
  await api.delete(`/gastos/${id}`)
  await cargarTodo()
}

function salir() {
  auth.cerrarSesion()
  router.push('/login')
}

onMounted(cargarTodo)
</script>

<template>
  <div class="layout">
    <div class="encabezado">
      <div>
        <h1>GastoClaro</h1>
        <p>Hola, {{ auth.usuario?.nombre }}</p>
      </div>
      <button class="boton-fantasma" @click="salir">Salir</button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="cargandoInicial" data-testid="skeleton" class="skeleton-grupo">
      <div class="skeleton tarjeta" style="height: 80px; margin-bottom: 1.5rem"></div>
      <div class="skeleton tarjeta" style="height: 140px; margin-bottom: 1.5rem"></div>
      <div class="skeleton tarjeta" style="height: 140px; margin-bottom: 1.5rem"></div>
      <div class="tarjeta">
        <div class="skeleton-linea" v-for="n in 3" :key="n"></div>
      </div>
    </div>

    <div v-else data-testid="contenido">
      <div class="tarjeta" style="margin-bottom: 1.5rem">
        <p>Total registrado</p>
        <p class="cifra">${{ totalMes.toFixed(2) }}</p>
      </div>

      <div class="tarjeta" style="margin-bottom: 1.5rem">
        <h2>Nueva categoría</h2>
        <form class="grid-form" @submit.prevent="crearCategoria">
          <input v-model="nuevaCategoria" placeholder="Ej. Comida" />
          <input v-model.number="presupuestoCategoria" type="number" min="0" step="0.01" placeholder="Presupuesto mensual (opcional)" />
          <button class="boton" type="submit">Agregar categoría</button>
        </form>
      </div>

      <div class="tarjeta" style="margin-bottom: 1.5rem">
        <h2>Registrar gasto</h2>
        <form class="grid-form" @submit.prevent="crearGasto">
          <input v-model="descripcionGasto" placeholder="Descripción" />
          <input v-model.number="montoGasto" type="number" min="0.01" step="0.01" placeholder="Monto" />
          <select v-model.number="categoriaGasto">
            <option :value="null" disabled>Elige categoría</option>
            <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
          </select>
          <button class="boton" type="submit">Agregar gasto</button>
        </form>
      </div>

      <div class="tarjeta">
        <h2>Movimientos</h2>
        <div v-if="gastos.length === 0">Todavía no registras gastos.</div>
        <div class="fila-gasto" v-for="g in gastos" :key="g.id">
          <div>
            <strong>{{ g.descripcion }}</strong>
            <div style="font-size: 0.85rem; opacity: 0.7">{{ nombreCategoria(g.categoria_id) }} · {{ new Date(g.fecha).toLocaleDateString() }}</div>
          </div>
          <div style="display:flex; align-items:center; gap:0.75rem">
            <span class="monto-negativo">-${{ g.monto.toFixed(2) }}</span>
            <button class="boton-fantasma" @click="eliminarGasto(g.id)">Borrar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
