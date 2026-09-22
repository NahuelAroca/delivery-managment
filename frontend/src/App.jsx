import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import DriverLogin from './pages/DriverLogin';
import RecordForm from './pages/RecordForm';
import AdminDashboard from './pages/AdminDashboard';
import RecordDetail from './pages/RecordDetail';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DriverLogin />} />
        <Route path="/submit-record" element={<RecordForm />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/record/:id" element={<RecordDetail />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
