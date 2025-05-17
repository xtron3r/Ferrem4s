$(document).ready(function () {
    $('#registerForm').validate({
        rules: {
            registerName: {
                required: true,
                minlength: 2,
            },
            registerLastName: {
                required: true,
                minlength: 2,
            },
            registerEmail: {
                required: true,
                email: true,
            },
            registerPassword: {
                required: true,
                minlength: 6,
            },
            confirmPassword: {
                required: true,
                equalTo: '#registerPassword',
            },
            registerPhone:{
                required: true,
                number: true,
            }
        },
        errorPlacement: function (error, element) {
            error.addClass("text-warning fw-semibold"); // Color y estilo
            error.insertAfter(element);
        },
        messages: {
            registerName: {
                required: "Por favor ingresa tu nombre",
                minlength: "Tu nombre debe tener al menos 2 caracteres",
            },
            registerLastName: {
                required: "Por favor ingresa tu apellido",
                minlength: "Tu apellido debe tener al menos 2 caracteres",
            },
            registerEmail: {
                required: "Por favor ingresa un correo electrónico",
                email: "Por favor ingresa un correo electrónico válido",
            },
            registerPassword: {
                required: "Por favor ingresa una contraseña",
                minlength: "La contraseña debe tener al menos 6 caracteres",
            },
            confirmPassword: {
                required: "Por favor confirma tu contraseña",
                equalTo: "Las contraseñas no coinciden",
            },
            registerPhone: {
                required: "Por favor ingresa tu número de teléfono",
                number: "Por favor ingresa un número de teléfono válido",
            }
        },
    });
});