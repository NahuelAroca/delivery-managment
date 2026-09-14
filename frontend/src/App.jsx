import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import DriverLogin from './pages/DriverLogin';
import RecordForm from './pages/RecordForm';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DriverLogin />} />
        <Route path="/submit-record" element={<RecordForm />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
