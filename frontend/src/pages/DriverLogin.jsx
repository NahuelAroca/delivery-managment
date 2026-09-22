import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { fetchDrivers } from '../api';

export default function DriverLogin() {
  const [drivers, setDrivers] = useState([]);
  const [selectedDriver, setSelectedDriver] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDrivers().then(data => {
      setDrivers(data);
      setIsLoading(false);
    });
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    if (!selectedDriver) return;
    
    // Guardamos la sesión en localStorage para persistencia básica
    const driver = drivers.find(d => d.id === parseInt(selectedDriver));
    localStorage.setItem('currentDriver', JSON.stringify(driver));
    
    // Navegamos al formulario principal
    navigate('/submit-record');
  };

  return (
    <div className="container" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="card" style={{ width: '100%' }}>
        <div className="text-center mb-6">
          <h1>Canhuel SRL</h1>
          <p className="mt-4">Bienvenido, por favor identifícate para continuar.</p>
        </div>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label className="form-label" htmlFor="driverSelect">Seleccionar Conductor</label>
            <select 
              id="driverSelect"
              className="form-control" 
              value={selectedDriver}
              onChange={(e) => setSelectedDriver(e.target.value)}
              disabled={isLoading}
              required
            >
              <option value="" disabled>-- Elige tu perfil --</option>
              {drivers.map(driver => (
                <option key={driver.id} value={driver.id}>
                  {driver.name}
                </option>
              ))}
            </select>
          </div>

          <button 
            type="submit" 
            className="btn btn-primary btn-full mt-6"
            disabled={!selectedDriver || isLoading}
          >
            Ingresar
          </button>
        </form>
      </div>
      
      <div className="mt-4 text-center">
        <Link to="/admin" style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '0.875rem' }}>
          Ingreso para Dueños (Panel de Control)
        </Link>
      </div>
    </div>
  );
}
