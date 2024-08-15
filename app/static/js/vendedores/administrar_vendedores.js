export async function cancelar_formulario() {
    const respuesta_servidor = await fetch('/cancelar_formulario', {
        method: 'POST',
        header: {
            'Content-Type': 'application/json'
        },
    });

    // Obtener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respuesta sea existosa
    if (respuesta.success) {

        // Redirigir a la página de anterior
        window.location.href = '/ver_vendedores';
        return;
    }
}

export async function suspender_o_activar_vendedor(identificador_vendedor, estado_vendedor){

    // Validar datos de entrada
    if(!identificador_vendedor || identificador_vendedor.trim() === '' || !estado_vendedor || estado_vendedor.trim() === '') {
        alert('Verifique que se estén enviando correctamente los datos')
        return;
    }

    // Elegir acción dependiendo del estado del vendedor
    let accion = estado_vendedor == 'False' ? 'activar': 'suspender'
    let nuevo_estado_vendedor = estado_vendedor == 'False' ? 'Activar': 'Suspender'

    // Lanzar advertencia de eliminación
    if (!confirm(`¿Está seguro de ${accion} este vendedor?`)){
        return;
    }

    // Realizar consulta al servidor enviando el identificador y el estado del vendedoer
    const respuesta_servidor = await fetch('/suspender_vendedor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_vendedor': identificador_vendedor, 'estado_vendedor': nuevo_estado_vendedor})
    });

    // Obtener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respuesta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        window.location.href = `/vendedor_especifico/${identificador_vendedor}`
        return;
    }
}

export async function eliminar_vendedor(identificador_vendedor) {

    // Verificar identificador
    if (!identificador_vendedor || identificador_vendedor.trim() === ''){
        alert('Verifique que se esté enviando correctamente los datos')
        return;
    }

    // Lanzar advertencia de eliminación
    if (!confirm('¿Está seguro de eliminar este vendedor?')) {
        return;
    }

    // Realizar consulta al servidor enviando el identificador del vendedor
    const respuesta_servidor = await fetch('/eliminar_vendedor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_vendedor': identificador_vendedor})
    })

    // Obtenener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respueta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        window.location.href = '/ver_vendedores'
        return;
    }
}