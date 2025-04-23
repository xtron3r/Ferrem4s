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
        },
        submitHandler: function (form) {
            $.ajax({
                url: "{% url 'login' %}",
                type: "POST",
                data: $(form).serialize(), // Serialize el formulario para enviar los datos correctamente
                success: function (response) {
                    // Redirecciona según la respuesta del servidor
                    window.location.href = response.redirect_url;
                },
                error: function (response) {
                    alert("Error: Correo electrónico o contraseña incorrectos.");
                }
            });
            return false; // Evita que el formulario se envíe normalmente
        }
    });
});
