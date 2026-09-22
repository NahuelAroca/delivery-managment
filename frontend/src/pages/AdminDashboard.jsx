import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchRecords, fetchDrivers } from '../api';

export default function AdminDashboard() {
  const [records, setRecords] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Filters
  const [driverId, setDriverId] = useState('');
  const [category, setCategory] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [driversData, recordsData] = await Promise.all([
        fetchDrivers(),
        fetchRecords({ driver_id: driverId, category, start_date: startDate, end_date: endDate })
      ]);
      setDrivers(driversData);
      setRecords(recordsData);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const getDriverName = (id) => {
    const d = drivers.find(drv => drv.id === id);
    return d ? d.name : `Driver ${id}`;
  };

  const getCategoryLabel = (cat) => {
    const labels = {
      remito: 'Remito',
      fuel: 'Combustible',
      general: 'General'
    };
    return labels[cat] || cat;
  };

  return (
    <div className="container" style={{ maxWidth: '1000px', paddingTop: '2rem' }}>
      <div className="flex items-center justify-between mb-6">
        <h1>Panel de Administración</h1>
        <Link to="/" className="btn btn-secondary">Ir al Login de Chofer</Link>
      </div>

      {/* Filters Panel */}
      <div className="card mb-6">
        <form 
          className="flex flex-col" 
          style={{ gap: '1rem', flexDirection: 'row', flexWrap: 'wrap', alignItems: 'flex-end' }}
          onSubmit={(e) => { e.preventDefault(); loadData(); }}
        >
          <div className="form-group" style={{ marginBottom: 0, flex: 1, minWidth: '150px' }}>
            <label className="form-label">Chofer</label>
            <select className="form-control" value={driverId} onChange={e => setDriverId(e.target.value)}>
              <option value="">Todos</option>
              {drivers.map(d => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </select>
          </div>
          
          <div className="form-group" style={{ marginBottom: 0, flex: 1, minWidth: '150px' }}>
            <label className="form-label">Categoría</label>
            <select className="form-control" value={category} onChange={e => setCategory(e.target.value)}>
              <option value="">Todas</option>
              <option value="remito">Remito</option>
              <option value="fuel">Combustible</option>
              <option value="general">Gasto General</option>
            </select>
          </div>

          <div className="form-group" style={{ marginBottom: 0, flex: 1, minWidth: '150px' }}>
            <label className="form-label">Desde</label>
            <input type="date" className="form-control" value={startDate} onChange={e => setStartDate(e.target.value)} />
          </div>

          <div className="form-group" style={{ marginBottom: 0, flex: 1, minWidth: '150px' }}>
            <label className="form-label">Hasta</label>
            <input type="date" className="form-control" value={endDate} onChange={e => setEndDate(e.target.value)} />
          </div>

          <button type="submit" className="btn btn-primary" style={{ height: '38px' }} disabled={isLoading}>
            Filtrar
          </button>
        </form>
      </div>

      {/* Records Table */}
      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        <table className="admin-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Fecha</th>
              <th>Chofer</th>
              <th>Categoría</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr>
                <td colSpan="5" className="text-center" style={{ padding: '2rem' }}>Cargando...</td>
              </tr>
            ) : records.length === 0 ? (
              <tr>
                <td colSpan="5" className="text-center" style={{ padding: '2rem' }}>No se encontraron registros.</td>
              </tr>
            ) : (
              records.map(record => (
                <tr key={record.id}>
                  <td>#{record.id}</td>
                  <td>{record.date}</td>
                  <td>{getDriverName(record.driver_id)}</td>
                  <td>
                    <span className={`badge badge-${record.category}`}>
                      {getCategoryLabel(record.category)}
                    </span>
                  </td>
                  <td>
                    <Link to={`/admin/record/${record.id}`} className="btn btn-secondary" style={{ padding: '0.25rem 0.75rem', fontSize: '0.75rem' }}>
                      Ver Detalles
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
