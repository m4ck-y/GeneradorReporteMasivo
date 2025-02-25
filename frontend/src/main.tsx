import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import TableComponent from './table.tsx'
import SearchCard from './search.tsx'
import { Space } from 'antd'
import { CampaniasProvider } from './context/CampaniasContext.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <CampaniasProvider>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <SearchCard />
        <TableComponent />
      </Space>
    </CampaniasProvider>
  </StrictMode>,
)
