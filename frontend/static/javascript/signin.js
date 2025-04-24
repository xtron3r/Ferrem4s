$(document).ready(function () {
    $("#loginForm").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required: true
            }
        },
        messages: {
            email: {
                required: "Por favor ingresa tu correo.",
                email: "Por favor ingresa un correo electrónico válido"
            },
            password: {
                required: "Por favor ingresa tu contraseña"
            }
        },
        errorPlacement: function (error, element) {
            error.addClass("text-warning fw-semibold"); // Color y estilo
            error.insertAfter(element);
        }
    });
});
