import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchRecordDetail, fetchDrivers } from '../api';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function RecordDetail() {
  const { id } = useParams();
  const [record, setRecord] = useState(null);
  const [driverName, setDriverName] = useState('Cargando...');
  const [error, setError] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        const detail = await fetchRecordDetail(id);
        setRecord(detail);
        
        // Fetch driver name
        const driversData = await fetchDrivers();
        const d = driversData.find(drv => drv.id === detail.driver_id);
        if (d) setDriverName(d.name);
        
      } catch (err) {
        setError('Error al cargar el detalle del registro.');
      }
    };
    loadData();
  }, [id]);

  if (error) {
    return (
      <div className="container mt-6">
        <div className="card text-center" style={{ color: 'var(--danger)' }}>
          {error}
          <br /><br />
          <Link to="/admin" className="btn btn-secondary">Volver</Link>
        </div>
      </div>
    );
  }

  if (!record) {
    return <div className="container mt-6 text-center">Cargando detalles...</div>;
  }

  const getCategoryLabel = (cat) => {
    const labels = {
      remito: 'Remito',
      fuel: 'Combustible',
      general: 'Gasto General'
    };
    return labels[cat] || cat;
  };

  return (
    <div className="container" style={{ maxWidth: '800px', paddingTop: '2rem', paddingBottom: '3rem' }}>
      <div className="flex items-center justify-between mb-6">
        <div>
          <Link to="/admin" style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '0.875rem' }}>&larr; Volver al Panel</Link>
          <h2 className="mt-4">Registro #{record.id}</h2>
        </div>
        <span className={`badge badge-${record.category}`}>{getCategoryLabel(record.category)}</span>
      </div>

      <div className="card mb-6">
        <h3>Información General</h3>
        <div className="detail-grid mt-4">
          <div className="detail-item">
            <span className="detail-label">Fecha del Remito/Gasto</span>
            <span className="detail-value">{record.date}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Subido al sistema</span>
            <span className="detail-value">{new Date(record.created_at + 'Z').toLocaleString('es-AR', { timeZone: 'America/Argentina/Buenos_Aires', dateStyle: 'short', timeStyle: 'short' })}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Chofer</span>
            <span className="detail-value">{driverName}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Categoría</span>
            <span className="detail-value">{getCategoryLabel(record.category)}</span>
          </div>
        </div>
      </div>

      <div className="card mb-6">
        <h3>Datos Específicos</h3>
        <div className="detail-grid mt-4">
          {record.category === 'remito' && (
            <>
              <div className="detail-item">
                <span className="detail-label">Lugar de Carga</span>
                <span className="detail-value">{record.loading_location}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Destino</span>
                <span className="detail-value">{record.destination}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Empresa</span>
                <span className="detail-value">{record.company}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Número de Remito</span>
                <span className="detail-value">{record.remito_number}</span>
              </div>
            </>
          )}

          {record.category === 'fuel' && (
            <div className="detail-item">
              <span className="detail-label">Litros Cargados</span>
              <span className="detail-value">{record.liters} L</span>
            </div>
          )}

          {record.category === 'general' && (
            <div className="detail-item">
              <span className="detail-label">Importe</span>
              <span className="detail-value">${record.amount}</span>
            </div>
          )}
        </div>
      </div>

      <div className="card">
        <h3>Fotografías Adjuntas ({record.photos?.length || 0})</h3>
        {record.photos && record.photos.length > 0 ? (
          <div className="photo-gallery mt-4">
            {record.photos.map(photo => {
              const photoUrl = `${API_URL}/records/photos/${photo.file_path}`;
              return (
                <div key={photo.id} className="photo-item">
                  <img src={photoUrl} alt={`Foto ${photo.id}`} />
                  <a href={photoUrl} target="_blank" rel="noopener noreferrer" className="btn btn-secondary btn-full mt-4">
                    Ver Original / Descargar
                  </a>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="mt-4">No hay fotografías para este registro.</p>
        )}
      </div>
    </div>
  );
}
