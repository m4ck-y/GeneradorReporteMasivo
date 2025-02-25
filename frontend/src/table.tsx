import React from 'react';
import { Space, Table, Tag, Button, Tooltip, message } from 'antd';
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

const TableComponent: React.FC = () => {
  const { 
    campanias, 
    loading, 
    pagination,
    checkReportStatus,
    downloadReport,
    fechaSelected,
    buscarCampanias
  } = useCampanias();

  const handleDownloadReport = async (id: number) => {
    try {
      const status = await checkReportStatus(id);
      if (status.estado === 'COMPLETADO' && status.ruta_archivo) {
        await downloadReport(status.ruta_archivo);
      } else {
        message.info('El reporte aún no está disponible');
      }
    } catch (error) {
      message.error('Error descargando el reporte');
      console.error('Error:', error);
    }
  };

  const handleTableChange = (page: number, pageSize: number) => {
    if (fechaSelected) {
      buscarCampanias(fechaSelected, page, pageSize);
    }
  };

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