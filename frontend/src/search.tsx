import React, { useEffect, useState } from 'react';
import { SearchOutlined, FileExcelOutlined } from '@ant-design/icons';
import { Button, Flex, Select, Space, Tooltip, Divider, message } from 'antd';
import { http } from './api/http';
import { useCampanias } from './context/CampaniasContext';
import { ReportResponse } from './types/reports';

interface FechasResponse {
  fechas: string[];
  total: number;
}

const SearchCard: React.FC = () => {
  const [fechas, setFechas] = useState<string[]>([]);
  const { 
    buscarCampanias, 
    setFechaSelected, 
    fechaSelected,
    campanias,
    loading,
    generatingReports,
    setGeneratingReports 
  } = useCampanias();

  useEffect(() => {
    http.get<FechasResponse>(`/campania/fechas`).then((response) => {
      setFechas(response.value?.fechas || []);
    });
  }, []);

  const onSearch = () => {
    if (fechaSelected) {
      buscarCampanias(fechaSelected);
    }
  };

  const handleChangeSelect = (value: string) => {
    setFechaSelected(value);
  };

  const handleGenerateReport = async () => {
    if (fechaSelected) {
      try {
        setGeneratingReports(true);
        const response = await http.get<ReportResponse>('/reporte', {
          fecha: fechaSelected
        });
        
        if (response.value) {
          message.success(response.value.mensaje);
          // Refrescar la tabla para mostrar estados actualizados
          buscarCampanias(fechaSelected);
        }
      } catch (error) {
        message.error('Error iniciando generación de reportes');
        console.error('Error:', error);
      } finally {
        setGeneratingReports(false);
      }
    }
  };

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Flex wrap gap="small" align="center">
        <Select
          placeholder='Fechas disponibles'
          style={{ width: 120 }}
          onChange={handleChangeSelect}
          options={fechas.map((fecha) => ({ value: fecha, label: fecha }))}
        />
        <Tooltip title="Buscar">
          <Button 
            type="primary" 
            shape="circle" 
            icon={<SearchOutlined />} 
            onClick={onSearch}
            loading={loading}
          />
        </Tooltip>
      </Flex>

      {campanias.length > 0 && (
        <>
          <Divider style={{ margin: '12px 0' }} />
          <Flex justify="end">
            <Tooltip title="Generar reporte de todos los registros">
              <Button
                type="primary"
                icon={<FileExcelOutlined />}
                onClick={handleGenerateReport}
                loading={generatingReports}
                disabled={loading}
              >
                Generar Reporte Masivo
              </Button>
            </Tooltip>
          </Flex>
        </>
      )}
    </Space>
  );
};

export default SearchCard;