import { ENDPOINT_BASE } from '../configuracion.js'

export async function eliminar_estado(identificador_estado) {

    // Verificar identificador
    if (!identificador_estado || identificador_estado.trim() === ''){
        alert('Verifique que se esté enviando correctamente los datos')
        return;
    }

    // Lanzar advertencia de eliminación
    if (!confirm('¿Está seguro de eliminar este estado?  (Se eliminará todo lo que contenga)')) {
        return;
    }

    // Realizar consulta al servidor enviando el identificador del vendedor
    const respuesta_servidor = await fetch('/eliminar_estado', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_estado': identificador_estado})
    })

    // Obtenener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respueta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        window.location.href = '/estados_republica'
        return;
    }
}

export async function eliminar_municipio(identificador_municipio) {

    // Verificar identificador
    if (!identificador_municipio || identificador_municipio.trim() === ''){
        alert('Verifique que se esté enviando correctamente los datos')
        return;
    }

    // Lanzar advertencia de eliminación
    if (!confirm('¿Está seguro de eliminar este municipio?  (Se eliminará todo lo que contenga)')) {
        return;
    }

    // Realizar consulta al servidor enviando el identificador del vendedor
    const respuesta_servidor = await fetch('/eliminar_municipio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_municipio': identificador_municipio})
    })

    // Obtenener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respueta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        let currentURL = window.location.href;
        window.location.href = currentURL;
        return;
    }
}

export async function eliminar_localidad(identificador_localidad) {

    // Verificar identificador
    if (!identificador_localidad || identificador_localidad.trim() === ''){
        alert('Verifique que se esté enviando correctamente los datos')
        return;
    }

    // Lanzar advertencia de eliminación
    if (!confirm('¿Está seguro de eliminar esta localidad?  (Se eliminará todo lo que contenga)')) {
        return;
    }

    // Realizar consulta al servidor enviando el identificador del vendedor
    const respuesta_servidor = await fetch('/eliminar_localidad', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_localidad': identificador_localidad})
    })

    // Obtenener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respueta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        let currentURL = window.location.href;
        window.location.href = currentURL;
        return;
    }
}

export async function eliminar_complejo(identificador_complejo) {

    // Verificar identificador
    if (!identificador_complejo || identificador_complejo.trim() === ''){
        alert('Verifique que se esté enviando correctamente los datos')
        return;
    }

    // Lanzar advertencia de eliminación
    if (!confirm('¿Está seguro de eliminar este complejo?  (Se eliminará todo lo que contenga)')) {
        return;
    }

    // Realizar consulta al servidor enviando el identificador del vendedor
    const respuesta_servidor = await fetch('/eliminar_complejo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_complejo': identificador_complejo})
    })

    // Obtenener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respueta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        let currentURL = window.location.href;
        window.location.href = currentURL;
        return;
    }
}

export async function eliminar_lote(identificador_lote, url) {

    // Verificar identificador
    if (!identificador_lote || identificador_lote.trim() === ''){
        alert('Verifique que se esté enviando correctamente los datos')
        return;
    }

    // Lanzar advertencia de eliminación
    if (!confirm('¿Está seguro de eliminar este lote?  (Se eliminará todo lo que contenga)')) {
        return;
    }

    // Realizar consulta al servidor enviando el identificador del vendedor
    const respuesta_servidor = await fetch('/eliminar_lote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_lote': identificador_lote})
    })

    // Obtenener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respueta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        window.location.href = url;
        return;
    }
}

// Función para obtener el token
export async function obtener_token(identificador) {
    try {

        // Realizar solicitud al servidor para cerrar sesión
        const respuesta_servidor = await fetch('/obtener_token_lote', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        // Obtener la respuesta
        const respuesta = await respuesta_servidor.json();

        // Verificar que la respuesta sea existosa
        if (respuesta.success) {

            // Obtener token
            let token = respuesta.token


            await anadir_valores(token, identificador)
        } else {

            // Aviso de error
            alert('No de pudo obtener los datos. Intente nuevamente.');
            window.location.href = '/editar_seccion';
        }
    } catch (error) {

        // Aviso de error
        alert('Ocurrió un error inesperado al intentar obtener el token.');
    }
}

async function anadir_valores(token, identificador) {

    try {

        const response = await fetch(`${ENDPOINT_BASE}/obtener_seccion_especifico/${identificador}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }); // Cambia la URL según tu API
        const data = await response.json();

        document.getElementById('nombre_seccion').value = data[0].nombre_seccion || '';
        document.getElementById('color_seccion').value = data[0].color_seccion || '#563d7c';
        document.getElementById('cantidad_lotes').value = data[0].cantidad_lotes || 1;
        document.getElementById('identificador_seccion').value = data[0].id_seccion || '';
        document.getElementById('id_complejo_residencial').value = data[0].id_complejo_residencial || '';


    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

export async function eliminar_seccion() {

    // Obtener identificador
    let identificador_seccion = document.getElementById('identificador_seccion').value;

    console.log(identificador_seccion)

    // Verificar identificador
    if (!identificador_seccion || identificador_seccion.trim() === ''){
        alert('Verifique que se esté enviando correctamente los datos')
        return;
    }

    // Lanzar advertencia de eliminación
    if (!confirm('¿Está seguro de eliminar esta sección?  (Se eliminará todo lo que contenga)')) {
        return;
    }

    // Realizar consulta al servidor enviando el identificador del vendedor
    const respuesta_servidor = await fetch('/eliminar_seccion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_seccion': identificador_seccion})
    })

    // Obtenener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respueta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        let currentURL = window.location.href;
        window.location.href = currentURL;
        return;
    }
}

export async function eliminar_url(objetivo) {

    // Verificar objetivio
    if (!objetivo || objetivo.trim() === '') {
        alert('Verifique que se esté enviando correctamente los datos')
        return;
    }

    // Realizar consulta al servidor para eliminar el objetivo
    const respuesta_servidor = await fetch('/eliminar_url_previa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'objetivo_url': objetivo})
    })
    // Obtener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respueta se exitosa
    if (respuesta.success) {

        let url_previa = respuesta.url_previa
        window.location.href = url_previa;
        return;
    }
}