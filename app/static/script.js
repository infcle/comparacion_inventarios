// Referencias a elementos del DOM
const uploadForm = document.getElementById("uploadForm");
const loadingSpinner = document.getElementById("loadingSpinner");
const resultsCard = document.getElementById("resultsCard");
const resultsContent = document.getElementById("resultsContent");
const downloadBtn = document.getElementById("downloadBtn");
const errorAlert = document.getElementById("errorAlert");
const successAlert = document.getElementById("successAlert");

let archivoResultado = null;

// Event Listeners
uploadForm.addEventListener("submit", handleFormSubmit);
downloadBtn.addEventListener("click", handleDownload);

/**
 * Maneja el envío del formulario
 */
async function handleFormSubmit(e) {
  e.preventDefault();

  // Obtener elementos del formulario
  const ingresosInput = document.getElementById("ingresos");
  const salidasInput = document.getElementById("salidas");
  const kardexInput = document.getElementById("kardex");
  const mesInput = document.getElementById("mes");

  // Validar que se seleccionaron archivos
  if (
    !ingresosInput.files[0] ||
    !salidasInput.files[0] ||
    !kardexInput.files[0]
  ) {
    showError("Por favor, selecciona los tres archivos");
    return;
  }

  if (!mesInput.value) {
    showError("Por favor, selecciona el mes");
    return;
  }

  // Preparar FormData
  const formData = new FormData();
  formData.append("ingresos", ingresosInput.files[0]);
  formData.append("salidas", salidasInput.files[0]);
  formData.append("kardex", kardexInput.files[0]);
  formData.append("mes", mesInput.value);

  // Mostrar spinner de carga
  hideAlerts();
  showLoader();

  try {
    // Enviar solicitud al servidor
    const response = await fetch("/api/procesar", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Error al procesar los archivos");
      hideLoader();
      return;
    }

    // Mostrar resultados
    displayResults(data.resultado, data.archivo);
    archivoResultado = data.archivo;
    showSuccess("¡Procesamiento completado exitosamente!");
    hideLoader();
  } catch (error) {
    showError(`Error de red: ${error.message}`);
    hideLoader();
  }
}

/**
 * Muestra los resultados en la interfaz
 */
function displayResults(resultado, archivo) {
  const html = `
        <div class="result-item success">
            <h3>✅ Coincidencias</h3>
            <div class="value">${resultado.coincidencias}</div>
        </div>
        <div class="result-item">
            <h3>🔍 Comparaciones</h3>
            <div class="value">${resultado.total_comparaciones}</div>
        </div>
        <div class="result-item warning">
            <h3>➕ Ingresos Sobrantes</h3>
            <div class="value">${resultado.ingresos_sobrantes}</div>
        </div>
        <div class="result-item warning">
            <h3>➖ Salidas Sobrantes</h3>
            <div class="value">${resultado.salidas_sobrantes}</div>
        </div>
        <div class="result-item danger">
            <h3>⚠️ Kardex Sobrantes</h3>
            <div class="value">${resultado.kerno_sobrantes}</div>
        </div>
    `;

  resultsContent.innerHTML = html;
  resultsCard.classList.remove("hidden");
}

/**
 * Maneja la descarga del archivo de resultados
 */
async function handleDownload() {
  if (!archivoResultado) {
    showError("No hay archivo para descargar");
    return;
  }

  try {
    downloadBtn.disabled = true;
    downloadBtn.textContent = "⏳ Descargando...";

    const response = await fetch(
      `/api/descargar/${encodeURIComponent(archivoResultado)}`
    );

    if (!response.ok) {
      showError("Error al descargar el archivo");
      return;
    }

    // Crear blob y descargar
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = archivoResultado;
    document.body.appendChild(link);
    link.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(link);

    showSuccess("¡Archivo descargado correctamente!");
  } catch (error) {
    showError(`Error al descargar: ${error.message}`);
  } finally {
    downloadBtn.disabled = false;
    downloadBtn.textContent = "⬇️ Descargar Archivo Excel";
  }
}

/**
 * Muestra el spinner de carga
 */
function showLoader() {
  loadingSpinner.classList.remove("hidden");
  resultsCard.classList.add("hidden");
}

/**
 * Oculta el spinner de carga
 */
function hideLoader() {
  loadingSpinner.classList.add("hidden");
}

/**
 * Muestra un mensaje de error
 */
function showError(message) {
  errorAlert.textContent = `❌ ${message}`;
  errorAlert.classList.remove("hidden");
  successAlert.classList.add("hidden");

  // Auto-ocultar después de 5 segundos
  setTimeout(() => {
    errorAlert.classList.add("hidden");
  }, 5000);
}

/**
 * Muestra un mensaje de éxito
 */
function showSuccess(message) {
  successAlert.textContent = `✅ ${message}`;
  successAlert.classList.remove("hidden");
  errorAlert.classList.add("hidden");

  // Auto-ocultar después de 5 segundos
  setTimeout(() => {
    successAlert.classList.add("hidden");
  }, 5000);
}

/**
 * Oculta todas las alertas
 */
function hideAlerts() {
  errorAlert.classList.add("hidden");
  successAlert.classList.add("hidden");
}
