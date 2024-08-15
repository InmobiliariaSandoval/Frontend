/* Archivo de funciones reutilizables para el apartado
frontend */

// Función que obtiene los valores del formulario
function obtenerValoresFormulario(formulario) {

    // Generar las variables para inicializar
    // el nuevo formulario
    const nuevoFormulario = document.getElementById(formulario);
    const informacionFormulario = new FormData(nuevoFormulario);
    const datosFormulario = {}

    // Añadir la clave y valor del formulario al nuevo diccionario
    informacionFormulario.forEach((valor, clave) => {
        datosFormulario[clave] = valor;
    });

    return datosFormulario
}

// Función para validar el correo electronico
function esCorreoValido(correo) {
    // Definir patrón de validación
    const patron = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    return patron.test(correo)
}

function esStringValido(dato) {
    // Definir patrón de validación
    const patron = /^[a-zA-Z\sáéíóúÁÉÍÓÚñÑ]+$/
    return patron.test(dato)
}

function esCodigoPostalValido(codigo_postal) {
    // Definir patrón de validación
    const patron = /^\d{5}$/
    return patron.test(codigo_postal)
}

function esCURPValido(curp) {
    // Definir el patrón de validación
   const patron = /^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$/;
   return patron.test(curp)

}

function esRFCValido(rfc) {
    // Definir patrón de validación
    const patron = /^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$/;
    return patron.test(rfc);
}

function esNumeroDecimalValido(numero) {
    const patron = /^[0-9]+(\.[0-9]+)?$/;
    return patron.test(numero);
}

function esNumeroValido(numero) {
    // Definir patrón de validación
    const patron = /^[0-9]+$/;
    return patron.test(numero);
}

function esNumeroTelefonoValido(telefono) {
    // Definir patrón de validación
    const patron = /^\d{10}$/
    return patron.test(telefono)
}

function esNombreSeccionValido(seccion) {
    // Definir patrón de validación
    const patron = /^Sección \d+$/
    return patron.test(seccion)
}

function esFechaValida(fecha) {
    // Definir patrón de validación
    const patron = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
    return patron.test(fecha)

}

export function validarFormulario(nombreFormulario) {

    // Valores del formulario
    const datos_formulario = obtenerValoresFormulario(nombreFormulario)

    // Constante de los errores
    const errores = {};

    // Iterar por cada elemento del diccionario (datos_formulario)
    for (const [campo, valor] of Object.entries(datos_formulario)) {

        // Verificar cada caso del campo
        switch(campo){
            case 'correo_electronico':
                if (!esCorreoValido(valor)){ errores[campo] = ' Correo electrónico no es válido' };
                break;
            case 'nombres_cliente':
            case 'nombres_vendedor':
            case 'primer_apellido_vendedor':
            case 'primer_apellido_cliente':
            case 'estado':
            case 'municipio':
            case 'colonia':
            case 'nombre_estado':
            case 'nombre_municipio':
            case 'nombre_localidad':
            case 'nombre_complejo':
            case 'calle':
            case 'estado_civil':
            case 'ocupacion':
            case 'tipo_pago':
            case 'estado_compra':
                if (!esStringValido(valor)) { errores[campo] = `${campo.replace(/_/g, ' ')} no es válido`};
                break;
            case 'nombre_seccion':
                if (!esNombreSeccionValido(valor)) { errores[campo] = 'Nombre de sección no válido' };
                break;
            case 'tipo_complejo':
                let tipos_validos = ['Fraccionamiento', 'Residencial', 'Privada']
                if (!esStringValido(valor) || !tipos_validos.includes(valor)) { errores[campo] = 'Tipo complejo no es válido'};
                break
            case 'segundo_apellido_vendedor':
            case 'segundo_apellido_cliente':
                if (valor && !esStringValido(valor)) { errores[campo] = ' El segundo apellido no es válido' };
                break;
            case 'numero_telefono':
            case 'telefono_contacto':
                if (valor && !esNumeroTelefonoValido(valor)) { errores[campo] = ' El número de télefono no es válido' };
                break;
            case 'codigo_postal':
                if (!esCodigoPostalValido(valor)) { errores[campo] = ' El código postal no es válido' };
                break;
            case 'RFC_vendedor':
                if (valor && !esRFCValido(valor)) { errores[campo] = ' El RFC no es válido' };
                break;
            case 'CURP_cliente':
                if (!esCURPValido(valor)) { errores[campo] = ' El CURP no es válido'};
                break;
            case 'id_estado':
            case 'cantidad_lotes':
            case 'id_estado':
            case 'id_municipio':
            case 'id_localidad':
            case 'id_complejo_residencial':
            case 'id_seccion':
            case 'numero_lote':
            case 'id_compra':
            case 'id_lote':
            case 'id_vendedor':
            case 'cantidad_total_plazos':
            case 'numero_plazo':
            case 'id_plazo':
            case 'id_detalle_pago':
                if (!esNumeroValido(valor)) { errores[campo] = `${campo.replace(/_/g, ' ')} no válido`};
                break;
            case 'medida_total':
            case 'medida_norte':
            case 'medida_sur':
            case 'medida_este':
            case 'medida_oeste':
            case 'precio_total':
            case 'precio_inicial':
            case 'enganche':
            case 'cantidad_esperada':
            case 'cantidad_dada':
            case 'total_compra':
                if (valor && !esNumeroDecimalValido(valor)) { errores[campo] = `${campo.replace(/_/g, ' ')} no válido`}
                break;
            case 'numero_exterior':
                if (valor && !esNumeroValido(valor)) { errores[campo] = `${campo.replace(/_/g, ' ')} no válido` };
                break;
            case 'fecha_esperada':
            case 'fecha_entrega':
                if (!esFechaValida(valor)) { errores[campo] = 'Fecha no válida'};
                break;
            default:
                break;
        }
    }

    return errores

}
