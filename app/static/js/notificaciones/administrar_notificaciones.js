export async function eliminar_todas_notificaciones(){

    // Lanzar advertencia de eliminación
    if (!confirm(`¿Está seguro de eliminar todas las notificaciones?`)){
        return;
    }

    // Realizar consulta al servidor
    const respuesta_servidor = await fetch('/eliminar_todas_notificaciones', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'accion': true})
    });

    // Obtener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respuesta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        window.location.href = '/ver_notificaciones'
        return;
    }
}

export async function eliminar_una_notificacion(identificador_notificacion) {

    // Verificar que no se envíen valores nulos
    if (!identificador_notificacion || identificador_notificacion.trim() === '') {
        alert('Verifique que se esté obteniendo los valores.')
        return;
    }

    // Lanzar advertencia de eliminación
    if (!confirm('¿Está seguro de eliminar esta notificación?')) {
        return;
    }

    // Realizar consulta al servidor enviando el identificador de la notificación
    const respuesta_servidor = await fetch('/eliminar_una_notificacion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_notificacion': identificador_notificacion})
    })

    // Obtenener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respueta sea exitosa
    if (respuesta.success) {
        // Redirigiar a la página correspondiente
        window.location.href = '/ver_notificaciones'
        return;
    }
}

export async function marcar_todas_como_leidas(){

    // Lanzar advertencia de eliminación
    if (!confirm(`¿Está seguro de marcar como leídas todas las notificaciones?`)){
        return;
    }

    // Realizar consulta al servidor
    const respuesta_servidor = await fetch('/marcar_todas_notificaciones', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'accion': true})
    });

    // Obtener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respuesta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        window.location.href = '/ver_notificaciones'
        return;
    }
}

export async function marcar_como_leido(identificador_notificacion){

    // Verificar que se esté obteniendo el identitifador correspondiente
    if (!identificador_notificacion || identificador_notificacion.trim() === '') {
        alert('Verifique que se esté obteniendo los valores.')
        return;
    }

    // Realizar consulta al servidor enviando el identiificador de la notificacion
    const respuesta_servidor = await fetch('/marcar_una_leida', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_notificacion': identificador_notificacion})
    });

    // Obtener respuesta del servidor
    const respuesta = respuesta_servidor.json()

    return respuesta.success
}