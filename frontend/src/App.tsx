import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import TicketListPage from './pages/TicketListPage'
import TicketFormPage from './pages/TicketFormPage'
import TicketDetailPage from './pages/TicketDetailPage'

const WorkspacePage = () => <div>工作台（开发中）</div>
const AILocatePage = () => <div>智能定位（开发中）</div>
const KnowledgeListPage = () => <div>知识库（开发中）</div>
const AdminPage = () => <div>管理后台（开发中）</div>

const App: React.FC = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/" element={<WorkspacePage />} />
          <Route path="/tickets" element={<TicketListPage />} />
          <Route path="/tickets/new" element={<TicketFormPage />} />
          <Route path="/tickets/:id" element={<TicketDetailPage />} />
          <Route path="/ai-locate" element={<AILocatePage />} />
          <Route path="/knowledge" element={<KnowledgeListPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Route>
      </Route>
    </Routes>
  </BrowserRouter>
)

export default App
