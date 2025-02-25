import React, { createContext, useContext, useState } from 'react';
import { http } from '../api/http';
import { ReportStatus } from '../types/reports';

interface Campania {
  id: number;
  nombre: string;
  fecha: string;
  estado: string;
  descripcion?: string;
}

interface PaginatedResponse {
  items: Campania[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

interface CampaniasContextType {
  campanias: Campania[];
  setCampanias: (campanias: Campania[]) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
  pagination: {
    total: number;
    page: number;
    pageSize: number;
    totalPages: number;
  };
  setPagination: (pagination: any) => void;
  fechaSelected: string | null;
  setFechaSelected: (fecha: string | null) => void;
  buscarCampanias: (fecha: string, page?: number, pageSize?: number) => Promise<void>;
  generatingReports: boolean;
  setGeneratingReports: (generating: boolean) => void;
  checkReportStatus: (campaignId: number) => Promise<ReportStatus>;
  downloadReport: (filePath: string) => Promise<void>;
}

const CampaniasContext = createContext<CampaniasContextType | undefined>(undefined);

export const CampaniasProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [campanias, setCampanias] = useState<Campania[]>([]);
  const [loading, setLoading] = useState(false);
  const [fechaSelected, setFechaSelected] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    pageSize: 10,
    totalPages: 0
  });
  const [generatingReports, setGeneratingReports] = useState(false);

  const buscarCampanias = async (fecha: string, page: number = 1, pageSize: number = 10) => {
    setLoading(true);
    try {
      const response = await http.get<PaginatedResponse>('/campania/list/', {
        fecha,
        page,
        page_size: pageSize
      });

      if (response.value) {
        setCampanias(response.value.items);
        setPagination({
          total: response.value.total,
          page: response.value.page,
          pageSize: response.value.page_size,
          totalPages: response.value.total_pages
        });
      }
    } catch (error) {
      console.error('Error buscando campañas:', error);
    } finally {
      setLoading(false);
    }
  };

  const checkReportStatus = async (campaignId: number): Promise<ReportStatus> => {
    const response = await http.get<ReportStatus>(`/reporte/status/${campaignId}`);
    return response.value!;
  };

  const downloadReport = async (filePath: string) => {
    try {
      const response = await http.get('/reports/download', { path: filePath }, true);
      if (response.value) {
        const url = window.URL.createObjectURL(new Blob([response.value as any]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filePath.split('/').pop() || 'reporte.csv');
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    } catch (error) {
      console.error('Error descargando reporte:', error);
    }
  };

  return (
    <CampaniasContext.Provider value={{
      campanias,
      setCampanias,
      loading,
      setLoading,
      pagination,
      setPagination,
      fechaSelected,
      setFechaSelected,
      buscarCampanias,
      generatingReports,
      setGeneratingReports,
      checkReportStatus,
      downloadReport,
    }}>
      {children}
    </CampaniasContext.Provider>
  );
};

export const useCampanias = () => {
  const context = useContext(CampaniasContext);
  if (context === undefined) {
    throw new Error('useCampanias must be used within a CampaniasProvider');
  }
  return context;
}; 