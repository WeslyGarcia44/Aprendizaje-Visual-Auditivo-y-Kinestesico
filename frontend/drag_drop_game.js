document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    const timerElement = document.getElementById("timer");
    const pieces = document.querySelectorAll(".draggable");
    let startTime = null;
    let timerInterval = null;
    let completedPieces = 0;

    // Función para iniciar el temporizador
    function startTimer() {
        startTime = new Date();
        timerInterval = setInterval(() => {
            const elapsedTime = Math.floor((new Date() - startTime) / 1000);
            timerElement.textContent = `Tiempo: ${elapsedTime}s`;
        }, 1000);
    }

    // Detener el temporizador y guardar el tiempo
    function stopTimer() {
        clearInterval(timerInterval);
        const elapsedTime = Math.floor((new Date() - startTime) / 1000);
        timerElement.textContent = `¡Completado en: ${elapsedTime}s!`;

        // Guardar tiempo en el backend
        const userId = localStorage.getItem("userId");
        fetch("http://127.0.0.1:5000/api/save-time", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ userId, exercise: "drag-drop", time: elapsedTime })
        }).catch(error => console.error("Error al guardar el tiempo:", error));
    }

    // Configuración de piezas arrastrables
    pieces.forEach(piece => {
        piece.addEventListener("dragstart", e => {
            e.dataTransfer.setData("text/plain", e.target.dataset.id);
        });
    });

    // Zona de arrastre
    dropZone.addEventListener("dragover", e => {
        e.preventDefault(); // Permitir soltar
    });

    dropZone.addEventListener("drop", e => {
        e.preventDefault();
        const id = e.dataTransfer.getData("text/plain");
        const target = e.target;

        // Verificar si el elemento se soltó en el lugar correcto
        if (target.dataset.id === id && !target.hasChildNodes()) {
            const piece = document.querySelector(`.draggable[data-id="${id}"]`);
            piece.style.position = "static";
            target.appendChild(piece);
            completedPieces++;

            // Verificar si el usuario completó el ejercicio
            if (completedPieces === pieces.length) {
                stopTimer();
            }
        }
    });

    // Iniciar el temporizador al cargar la página
    startTimer();
});
