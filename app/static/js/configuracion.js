// Endpoint base
// Comentar en caso de ser utilizado en local
export const ENDPOINT_BASE = "https://backendinmobiliariagruposandoval.zeabur.app/";

// Descomentar en caso de que se utilice en local
//export const ENDPOINT_BASE = "http://127.0.0.1:8000";

// Endpoint valir token acceso
export const ENDPOINT_VALIDAR_TOKEN = `${ENDPOINT_BASE}/`

// Endpoint para obtener el token de acceso
export const ENDPOINT_TOKEN_SESION = `${ENDPOINT_BASE}/token/`;
export const ENDPOINT_TOKEN_REINICIAR = `${ENDPOINT_BASE}/reiniciar_sesion`

// Endpoint para obtener todos los estados
export const ENDPOINT_OBTENER_ESTADOS = `${ENDPOINT_BASE}/estados_republica`;

// Endpoint para obtener todas las notificaciones
export const ENDPOINT_OBTENER_NOTIFICACIONES = `${ENDPOINT_BASE}/notificaciones`;
