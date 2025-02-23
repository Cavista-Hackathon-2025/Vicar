
import './App.css'
import { Routes, Route } from 'react-router-dom'
import { Dashboard } from './pages/auth/dashboard'
import { Inventory } from './pages/auth/inventory'
import { Sales } from './pages/auth/sales'
import { Index } from './pages'
export const App = () => {
  return (
    <>
      <Routes >
        <Route path="/" element={<Index />} />
        <Route path="dashboard" element={<Dashboard />}>
          <Route index element={<Inventory />} />
          <Route path="/sales" element={<Sales />} />
        </Route>
      </Routes>
    </>

  )


}

export default App
