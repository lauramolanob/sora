document.addEventListener('DOMContentLoaded', () => {
    const descripcionInput = document.getElementById('descripcion');
    const generarBoton = document.getElementById('generar');
    const listaNombres = document.getElementById('lista-nombres');

    generarBoton.addEventListener('click', async () => {
        const descripcion = descripcionInput.value.trim();
        if (descripcion) {
            listaNombres.innerHTML = `
                <div class="spinner-border text-primary" role="status">
                    <span class="sr-only">Cargando...</span>
                </div>
            `;

            try {
                const response = await fetch('http://127.0.0.1:5000/generar_nombres', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ descripcion })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    listaNombres.innerHTML = `<li class="list-group-item list-group-item-danger">Error: ${errorData.error || 'Error desconocido'}</li>`;
                    return;
                }

                const data = await response.json();
                listaNombres.innerHTML = ''; // Limpiar el indicador de carga

                if (data.nombres && Array.isArray(data.nombres)) {
                    data.nombres.forEach(nombre => {
                        const li = document.createElement('li');
                        li.className = 'list-group-item';
                        li.textContent = nombre;
                        listaNombres.appendChild(li);
                    });
                } else {
                    listaNombres.innerHTML = '<li class="list-group-item list-group-item-warning">No se recibieron nombres válidos.</li>';
                }

            } catch (error) {
                listaNombres.innerHTML = `<li class="list-group-item list-group-item-danger">Error de conexión: ${error.message}</li>`;
            }
        } else {
            listaNombres.innerHTML = '<li class="list-group-item list-group-item-warning">Por favor, introduce una descripción.</li>';
        }
    });
});