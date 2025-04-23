$(document).ready(function () {
    $('#registerForm').validate({
        rules: {
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
        },
        messages: {
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
        },
        // AQUI VA INFO
    });
});