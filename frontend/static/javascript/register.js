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
        errorElement: 'div',
        errorPlacement: function (error, element) {
            error.addClass('invalid-feedback');
            element.closest('.form-group').append(error);
        },
        highlight: function (element, errorClass, validClass) {
            $(element).addClass('is-invalid');
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).removeClass('is-invalid');
        },
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var registerForm = document.getElementById('registerForm');

    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault(); 

            var registerNameInput = document.getElementById('registerName');
            var registerEmailInput = document.getElementById('registerEmail');
            var registerPasswordInput = document.getElementById('registerPassword');
            var confirmPasswordInput = document.getElementById('confirmPassword');

            if (registerNameInput && registerEmailInput && registerPasswordInput && confirmPasswordInput) {
                if (registerPasswordInput.value === confirmPasswordInput.value) {
                    registerForm.submit();
                } else {
                    var passwordFeedback = document.getElementById('passwordFeedback');
                    if (passwordFeedback) {
                        passwordFeedback.textContent = 'Las contraseñas no coinciden.';
                    }
                }
            } else {
                console.error('Algunos elementos del formulario no existen.');
            }
        });
    } else {
        console.error('El formulario de registro no se encontró.');
    }
});