import {Route, Routes, Navigate} from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard';
import Register from './pages/Register';

function App() {
  return (
    <Routes>
      <Route path='/' element={<Navigate to='/login' />} />
      <Route path='/login' element={<Login />} />
      <Route path='/dashboard' element={<Dashboard />} />
      <Route path='/register' element={<Register />} />
    </Routes>  
  )
}

export default App;
