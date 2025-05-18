document.addEventListener("DOMContentLoaded", function () {
            const regionSelect = document.getElementById("region");
            const comunaSelect = document.getElementById("comuna");

            fetch("https://my.api.mockaroo.com/users.json?key=d8c0f870") 
            .then(response => response.json())
            .then(data => {
                const regiones = data.regiones;

                // Rellenar el select de regiones
                regiones.forEach(regionObj => {
                const option = document.createElement("option");
                option.value = regionObj.region;
                option.textContent = regionObj.region;
                regionSelect.appendChild(option);
                });

                // Escuchar cambios en región para actualizar comunas
                regionSelect.addEventListener("change", () => {
                const regionSeleccionada = regionSelect.value;
                const region = regiones.find(r => r.region === regionSeleccionada);

                // Limpiar comuna actual
                comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';

                if (region) {
                    region.comunas.forEach(comuna => {
                    const option = document.createElement("option");
                    option.value = comuna;
                    option.textContent = comuna;
                    comunaSelect.appendChild(option);
                    });
                }
                });
            })
            .catch(error => {
                console.error("Error al cargar regiones:", error);
            });
        });