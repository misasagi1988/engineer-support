import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import TicketListPage from './pages/TicketListPage'
import TicketFormPage from './pages/TicketFormPage'
import TicketDetailPage from './pages/TicketDetailPage'
import AILocatePage from './pages/AILocatePage'

import WorkspacePage from './pages/WorkspacePage'
import KnowledgeListPage from './pages/KnowledgeListPage'
import KnowledgeDetailPage from './pages/KnowledgeDetailPage'
import AdminPage from './pages/AdminPage'

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
          <Route path="/knowledge/:id" element={<KnowledgeDetailPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Route>
      </Route>
    </Routes>
  </BrowserRouter>
)

export default App
