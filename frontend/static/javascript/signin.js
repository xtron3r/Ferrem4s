$(document).ready(function () {
    $("#loginForm").validate({
        rules: {
            username: {
                required: true,
                email: true
            },
            password: {
                required: true
            }
        },
        messages: {
            username: {
                required: "Por favor ingresa tu usuario."
            },
            password: {
                required: "Por favor ingresa tu contraseña"
            }
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
