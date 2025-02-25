import React, { useEffect, useState } from 'react';
import { SearchOutlined } from '@ant-design/icons';
import { Button, Flex, Select, Space, Tooltip } from 'antd';
import { http } from './api/http';
import { useCampanias } from './context/CampaniasContext';

interface FechasResponse {
  fechas: string[];
  total: number;
}

const SearchCard: React.FC = () => {
  const [fechas, setFechas] = useState<string[]>([]);
  const { buscarCampanias, setFechaSelected, fechaSelected } = useCampanias();

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

  return (
    <Space direction="vertical">
      <Flex wrap gap="small">
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
          />
        </Tooltip>
      </Flex>
    </Space>
  );
};

export default SearchCard;