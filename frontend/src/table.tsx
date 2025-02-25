import React from 'react';
import { Space, Table, Tag, Button, Tooltip } from 'antd';
import type { TableProps } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import { useCampanias } from './context/CampaniasContext';
import { http } from './api/http';

interface Campania {
  id: number;
  nombre: string;
  fecha: string;
  estado: string;
  descripcion?: string;
}

const columns: TableProps<Campania>['columns'] = [
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
    width: '10%',
  },
  {
    title: 'Nombre',
    dataIndex: 'nombre',
    key: 'nombre',
    width: '25%',
  },
  {
    title: 'Descripción',
    dataIndex: 'descripcion',
    key: 'descripcion',
    width: '30%',
  },
  {
    title: 'Estado',
    dataIndex: 'estado',
    key: 'estado',
    width: '15%',
    render: (estado: string) => {
      let color = 'green';
      if (estado === 'EN PROCESO') color = 'orange';
      if (estado === 'PENDIENTE') color = 'gold';
      if (estado === 'COMPLETADO') color = 'blue';
      return <Tag color={color}>{estado}</Tag>;
    },
  },
  {
    title: 'Acciones',
    key: 'action',
    width: '20%',
    render: (_, record) => (
      <Space size="middle">
        <Tooltip title={record.estado !== 'COMPLETADO' ? 'El reporte aún no está disponible' : 'Descargar reporte'}>
          <Button
            type="primary"
            icon={<DownloadOutlined />}
            disabled={record.estado !== 'COMPLETADO'}
            onClick={() => handleDownloadReport(record.id)}
            size="small"
          >
            Descargar
          </Button>
        </Tooltip>
      </Space>
    ),
  },
];

const handleDownloadReport = async (id: number) => {
  try {
    const response = await http.get(`/reports/campaign/${id}`, {}, true);
    if (response.value) {
      const url = window.URL.createObjectURL(new Blob([response.value as any]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `reporte_campania_${id}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    }
  } catch (error) {
    console.error('Error descargando reporte:', error);
  }
};

const TableComponent: React.FC = () => {
  const { 
    campanias, 
    loading, 
    pagination, 
    buscarCampanias,
    fechaSelected
  } = useCampanias();

  const handleTableChange = (page: number, pageSize: number) => {
    if (fechaSelected) {
      buscarCampanias(fechaSelected, page, pageSize);
    }
  };

  return (
    <Table<Campania>
      columns={columns}
      dataSource={campanias}
      loading={loading}
      rowKey="id"
      pagination={{
        total: pagination.total,
        pageSize: pagination.pageSize,
        current: pagination.page,
        showSizeChanger: true,
        showTotal: (total) => `Total ${total} campañas`,
        onChange: handleTableChange,
        pageSizeOptions: [10, 20, 30, 50],
      }}
    />
  );
};

export default TableComponent;