export function calcularPlazos() {
    // Obtener los valores principales
    // Precio de la compra
    // Enganche de la compra
    // Plazos
    const precioTotal = parseFloat(document.getElementById('precio_inicial').value)
    const enganche = parseFloat(document.getElementById('enganche').value)
    const plazos = parseInt(document.getElementById('cantidad_total_plazos').value)
    const estadoCompra = document.getElementById('compra_completa').checked;

    // Verificar que se estén pasando los valores correspondientes
    if (isNaN(precioTotal) || isNaN(enganche) || isNaN(plazos)) {
        alert('Por favor, ingrese valores válidos en todos los campos');
        return;
    }

    // Obtener el monto final y los pagos mensuales
    const montoFinanciado = precioTotal - enganche;
    const pagoMensual = montoFinanciado / plazos;

    // Añadir los valores a la tabla
    const detallePagos = document.getElementById('detalle_pagos');
    detallePagos.innerHTML = '';

    document.getElementById('estado_compra').value = 'Proceso';
    document.getElementById('precio_total').value = montoFinanciado.toFixed(1);
    document.getElementById('pago_plazo').value = pagoMensual.toFixed(1);


    if (estadoCompra) {
        // Asignar el valor

        document.getElementById('estado_compra').value = 'Finalizado'
        console.log(document.getElementById('estado_compra').value)

        return;
     }


    // Añadir cada fila
    for (let i = 1; i <= plazos; i++) {
        const row = document.createElement('tr');

        const cellFecha = document.createElement('td');
        const fecha = new Date();
        fecha.setMonth(fecha.getMonth() + i);
        cellFecha.textContent = fecha.toLocaleDateString();
        row.appendChild(cellFecha);

        const cellMes = document.createElement('td');
        cellMes.textContent = `Mes ${i}`;
        row.appendChild(cellMes);

        const cellCantidad = document.createElement('td');
        cellCantidad.textContent = `$${pagoMensual.toFixed(1)}`;
        row.appendChild(cellCantidad);

        detallePagos.appendChild(row);
    }

}

export async function cancelar_formulario() {
    const respuesta_servidor = await fetch('/cancelar_formulario_venta', {
        method: 'POST',
        header: {
            'Content-Type': 'application/json'
        },
    });

    // Obtener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respuesta sea existosa
    if (respuesta.success) {
        return;
    }
}

export async function eliminar_url_pago(objetivo) {

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
        return;
    }
}

export async function eliminar_plazo(identificador_plazo, identificador_compra) {

    // Verificar los valores
    if (!identificador_plazo || identificador_plazo.trim() === '') {
        alert('Verifique que se esté enviando correctamente los daots');
        return;
    }

    // Lanzar advertencia de eliminación
    if (!confirm('¿Está seguro de eliminar este plazo? (Se eliminará todo lo que contenga)')) {
        return;
    }

    // Realizar consulta al servidor enviando el identificador
    const respuesat_plazo = await fetch('/eliminar_plazo', {
        method: 'POST',
        headers: {
            'Content-Type' :'application/json'
        },
        body: JSON.stringify({
            'identificador_plazo': identificador_plazo,
            'identificador_compra': identificador_compra
        })
    })

    // Obtener respuesta del servidor
    const respuesta = await respuesat_plazo.json()

    // Verificar respuesta exitosa
    if (respuesta.success) {

        // Redirigir a la página correspondiente
        window.location.href = `/resumen_compra/${identificador_compra}`;
        return;
    }
}

export async function cambiar_estado_compra(identificador_compra, estado_compra){

    // Validar datos de entrada
    if(!identificador_compra || identificador_compra.trim() === '' || !estado_compra || estado_compra.trim() === '') {
        alert('Verifique que se estén enviando correctamente los datos')
        return;
    }

    let accion = '';

    // Elegir acción dependiendo del estado del vendedor
    if (estado_compra == 'Finalizado') {
        accion = 'finalizar'
    } else if (estado_compra == 'Cancelado') {
        accion = 'cancelar'
    } else if (estado_compra == 'Proceso') {
        accion = 'reactivar'
    }

    // Lanzar advertencia de eliminación
    if (!confirm(`¿Está seguro de ${accion} esta venta?`)){
        return;
    }

    // Realizar consulta al servidor enviando el identificador y el estado del vendedoer
    const respuesta_servidor = await fetch('/cambiar_estado_compra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_compra': identificador_compra, 'estado_compra': estado_compra})
    });

    // Obtener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respuesta sea exitosa
    if (respuesta.success) {

        // Redirigiar a la página correspondiente
        window.location.href = `/resumen_compra/${identificador_compra}`
        return;
    }
}

export async function eliminar_detalle(identificador_detalle, url_previa) {

    // Verificar identificador
    if (!identificador_detalle || identificador_detalle.trim() === '') {
        alert('Verifique que se esté enviando correctamente los datos')
        return;
    }

    // Lanzar advertencia de eliminación
    if (!confirm('¿Está seguro de eliminar este detalle de plazo?')) {
        return;
    }

    // Realizar consulta al servidor enviando al identificador del detalle
    const respuesta_servidor = await fetch('/eliminar_detalle_pago', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'identificador_detalle': identificador_detalle})
    });

    // Obtener respuesta del servidor
    const respuesta = await respuesta_servidor.json()

    // Verificar que la respuesta sea exitosa
    if (respuesta.success) {

        // Reridigir a la página correspondiente
        window.location.href = url_previa;
        return;
    }
}