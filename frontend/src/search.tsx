import React, { useEffect, useState } from 'react';
import { SearchOutlined, FileExcelOutlined } from '@ant-design/icons';
import { Button, Flex, Select, Space, Tooltip, Divider } from 'antd';
import { http } from './api/http';
import { useCampanias } from './context/CampaniasContext';

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
    loading 
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
        const response = await http.get('/reports/generate-by-date', {
          fecha: fechaSelected
        }, true);
        
        // Si el backend retorna un blob, descargarlo
        if (response.value) {
          const url = window.URL.createObjectURL(new Blob([response.value as any]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', `reporte_${fechaSelected.replace('/', '')}.csv`);
          document.body.appendChild(link);
          link.click();
          link.remove();
        }
      } catch (error) {
        console.error('Error generando reporte:', error);
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
                loading={loading}
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