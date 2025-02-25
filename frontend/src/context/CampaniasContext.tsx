import React, { createContext, useContext, useState } from 'react';
import { http } from '../api/http';

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
      buscarCampanias
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