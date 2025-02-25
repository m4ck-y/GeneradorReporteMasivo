export interface ReportStatus {
  id_campana: number;
  estado: 'PENDIENTE' | 'EN PROCESO' | 'COMPLETADO' | 'ERROR';
  fecha: string;
  ruta_archivo: string | null;
}

export interface ReportResponse {
  mensaje: string;
  campanias: {
    id: number;
    nombre: string;
    estado: string;
  }[];
} 