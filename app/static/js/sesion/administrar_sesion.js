import { ENDPOINT_TOKEN_SESION, ENDPOINT_TOKEN_REINICIAR } from "../configuracion.js";

// Función para iniciar sesión
export async function iniciar_sesion() {
    // Obtener el correo y la contraseña para el inicio de sesión
    const correo_electronico = document.getElementById('correo_electronico_sesion').value.trim();
    const contraseña = document.getElementById('contraseña_sesion').value.trim();

    // Verificar que se ingrese correo y contraseña
    if (!correo_electronico || !contraseña) {
        alert('Por favor, ingrese el correo electrónico y la contraseña');
        return;
    }

    // Validar el formato del correo electrónico
    const patron_correo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!patron_correo.test(correo_electronico)) {

        // Aviso de error
        alert('Por favor, ingrese un correo electrónico válido.');
        return;
    }

    try {
        // Realizar solicitud a la API
        const respuesta = await fetch(ENDPOINT_TOKEN_SESION, {
            method: 'GET',
            headers: {
                'Authorization': 'Basic ' + btoa(`${correo_electronico}:${contraseña}`)
            }
        });


        // Verificar estado de la respuesta
        if (respuesta.ok) {
            // Obtener datos de la API
            const datos = await respuesta.json();

            // Verificar que se haya recibido un token
            if (datos.Token) {

                // Obtener token
                let token = datos.Token;
                let nombre_usuario = datos.Nombre_usuario

                // Enviar el token de sesión
                await enviar_token_servidor(token, nombre_usuario);

            } else {

                // Aviso de error
                alert('La respuesta no contiene un token válido.');
                return;
            }
        } else {
            const mensaje = await respuesta.json()
            // Manejo de diferentes códigos de estado
            switch (respuesta.status) {
                case 401:
                    alert(mensaje.detail);
                    break;
                case 403:
                    alert(mensaje.detail);
                    break;
                case 500:
                    alert(mensaje.detail);
                    break;
                default:
                    alert('Error desconocido. Intente nuevamente.');
            }
        }
    } catch (error) {

        // Aviso de error
        console.error('Error al iniciar sesión:', error);
        alert('Ocurrió un error al comunicarse con el servidor. Por favor, intente nuevamente más tarde.');
    }
}

// Función para enviar el token al servidor
async function enviar_token_servidor(token_acceso, nombre_usuario) {

    // Verificar que se esté enviando un token válido
    if (!token_acceso || token_acceso.trim() === '') {
        alert('Verifique que se esté obteniendo los valores.')
        return;
    }

    try {

        // Realizar solicitud al servidor enviando el token de acceso
        const respuesta_servidor = await fetch('/', {
            method : 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({token: token_acceso, usuario: nombre_usuario})
        });

        // Obtener respuesta
        const respuesta = await respuesta_servidor.json();

        // Verificar que la respuesta sea exitosa
        if(respuesta.success) {

            // Redireccionar al index
            window.location.href = '/resumen';
        } else {
            alert('Ocurrió un al comunicarse con el servidor. Intente nuevamente más tarde');
        }

    } catch (error) {

        // Aviso de error
        console.error('Error: ', error);
        alert('Ocurrió un error inesperado. Intenete nuevamente más tarde.')
    }
}

// Función para cerrar sesión
export async function cerrar_sesion() {
    try {

        // Realizar solicitud al servidor para cerrar sesión
        const respuesta_servidor = await fetch('/cerrar_sesion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        // Obtener la respuesta
        const respuesta = await respuesta_servidor.json();

        // Verificar que la respuesta sea existosa
        if (respuesta.success) {

            // Redirigir a la página de inicio de sesión
            window.location.href = '/';
        } else {

            // Aviso de error
            alert('No de pudo cerrar sesión correctamente. Intente nuevamente.');
            window.location.href = '/resumen';
        }
    } catch (error) {

        // Aviso de error
        alert('Ocurrió un error inesperado al intentar cerrar la sesión.');
    }
}

// Función para reiniciar sesión
export async function reiniciar_sesion() {

    // Obtener el correo, contraseña y frase para validar el usuario
    const correo_electronico = document.getElementById('correo_electronico_sesion').value.trim();
    const contraseña = document.getElementById('contraseña_sesion').value.trim();

    // Verificar que se ingrese correo y contraseña
    if (!correo_electronico || !contraseña) {
        alert('Ingrese el correo electrónico y la contraseña.');
        return;
    }

    // Validar el formato del correo electrónico
    const patron_correo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!patron_correo.test(correo_electronico)) {

        // Aviso de error
        alert('Por favor, ingrese un correo electrónico válido.');
        return;
    }

    // Obtener palabra de acceso
    const palabra_acceso = prompt("Ingresa tu palabra secreta de acceso")

    // Validar palabra de acceso
    if (!palabra_acceso || palabra_acceso.trim === ''){
        alert("Ingrese su palabra de acceso")
        return;
    }

    // Generar query params
    const parametros = {
        frase: palabra_acceso
    };

    try {
        // Realizar solicitud a la API
        const respuesta = await fetch(`${ENDPOINT_TOKEN_REINICIAR}?` + new URLSearchParams(parametros).toString(), {
            method: 'GET',
            headers: {
                'Authorization': 'Basic ' + btoa(`${correo_electronico}:${contraseña}`)
            },
        });

        // Verificar estado de la respuesta
        if (respuesta.ok) {
            // Obtener datos de la API
            const datos = await respuesta.json();

            // Verificar que se haya recibido un token
            if (!datos.success) {
                // Validar respuesta
                alert('No se logró reiniciar sesión, intente nuevamente más tarde.');
                return;
            }

            alert('Se reinició la sesión correctamente')

        } else {
            const mensaje = await respuesta.json()
            // Manejo de diferentes códigos de estado
            switch (respuesta.status) {
                case 400:
                    alert(mensaje.detail);
                    break;
                case 404:
                    alert(mensaje.detail);
                    break;
                case 500:
                    alert(mensaje.detail);
                    break;
                default:
                    alert('Error desconocido. Intente nuevamente.');
            }
        }
    } catch (error) {
        // Aviso de error
        alert('Ocurrió un error al comunicarse con el servidor. Por favor, intente nuevamente más tarde.');
    }
}