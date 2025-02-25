import React from 'react';
import { Space, Table, Tag } from 'antd';
import type { TableProps } from 'antd';
import { useCampanias } from './context/CampaniasContext';

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
  },
  {
    title: 'Nombre',
    dataIndex: 'nombre',
    key: 'nombre',
  },
  {
    title: 'Estado',
    dataIndex: 'estado',
    key: 'estado',
    render: (estado: string) => {
      let color = 'green';
      if (estado === 'PAUSADO') color = 'orange';
      if (estado === 'COMPLETADO') color = 'blue';
      return <Tag color={color}>{estado}</Tag>;
    },
  },
  {
    title: 'Descripción',
    dataIndex: 'descripcion',
    key: 'descripcion',
  },
  {
    title: 'Acciones',
    key: 'action',
    render: (_, record) => (
      <Space size="middle">
        <a onClick={() => console.log('Generar reporte', record.id)}>
          Generar Reporte
        </a>
      </Space>
    ),
  },
];

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