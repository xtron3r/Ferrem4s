document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form');
    var shippingInfo = document.getElementById('shipping-info');
    var paymentInfo = document.getElementById('payment-info');

    // Validar formulario antes de enviarlo
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        console. Log('Form submitted...')

        // Validar campos de envío
        var address = document.querySelector('input[name="address"]').value;
        var city = document.querySelector('input[name="city"]').value;
        var state = document.querySelector('input[name="state"]').value;
        var zipcode = document.querySelector('input[name="zipcode"]').value;
        var country = document.querySelector('input[name="country"]').value;

        if (!address || !city || !state || !zipcode || !country) {
            alert('Por favor, complete todos los campos de envío.');
            return;
        }

        // Validar campos de tarjeta de crédito
        var numeroTarjeta = document.querySelector('input[name="numeroTarjeta"]').value;
        var nombreTitular = document.querySelector('input[name="nombreTitular"]').value;
        var fechaCaducidad = document.querySelector('input[name="fechaCaducidad"]').value;
        var codigoCvc = document.querySelector('input[name="codigoCvc"]').value;

        if (!numeroTarjeta || !nombreTitular || !fechaCaducidad || !codigoCvc) {
            alert('Por favor, complete todos los campos de tarjeta de crédito.');
            return;
        }

        // Si pasa la validación, enviar formulario
        form.submit();
    });
});


