import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Upload, X, CheckCircle, ArrowLeft } from 'lucide-react';
import { createRecord } from '../api';

export default function RecordForm() {
  const navigate = useNavigate();
  const [driver, setDriver] = useState(null);
  const [category, setCategory] = useState('');
  
  // Base fields
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  
  // Specific fields
  const [loadingLocation, setLoadingLocation] = useState('');
  const [destination, setDestination] = useState('');
  const [company, setCompany] = useState('');
  const [remitoNumber, setRemitoNumber] = useState('');
  const [liters, setLiters] = useState('');
  const [amount, setAmount] = useState('');
  
  // Photos
  const [photos, setPhotos] = useState([]);
  const fileInputRef = useRef(null);
  
  // Status
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const saved = localStorage.getItem('currentDriver');
    if (!saved) {
      navigate('/');
    } else {
      setDriver(JSON.parse(saved));
    }
  }, [navigate]);

  const handlePhotoSelect = (e) => {
    const files = Array.from(e.target.files);
    if (photos.length + files.length > 2) {
      setError('Máximo 2 fotografías permitidas.');
      return;
    }
    
    const newPhotos = files.map(file => ({
      file,
      preview: URL.createObjectURL(file)
    }));
    
    setPhotos([...photos, ...newPhotos]);
    setError('');
  };

  const removePhoto = (index) => {
    const newPhotos = [...photos];
    URL.revokeObjectURL(newPhotos[index].preview);
    newPhotos.splice(index, 1);
    setPhotos(newPhotos);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!category) {
      setError('Por favor selecciona una categoría.');
      return;
    }
    if (photos.length === 0) {
      setError('Debes subir al menos 1 fotografía.');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('driver_id', driver.id);
      formData.append('category', category);
      formData.append('date', date);

      if (category === 'remito') {
        formData.append('loading_location', loadingLocation);
        formData.append('destination', destination);
        formData.append('company', company);
        formData.append('remito_number', remitoNumber);
      } else if (category === 'fuel') {
        formData.append('liters', liters);
      } else if (category === 'general') {
        formData.append('amount', amount);
      }

      photos.forEach(photo => {
        formData.append('photos', photo.file);
      });

      await createRecord(formData);
      setSuccess(true);
    } catch (err) {
      setError(err.message || 'Error al enviar el registro.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const resetForm = () => {
    setCategory('');
    setLoadingLocation('');
    setDestination('');
    setCompany('');
    setRemitoNumber('');
    setLiters('');
    setAmount('');
    setPhotos([]);
    setSuccess(false);
    setError('');
  };

  if (!driver) return null;

  if (success) {
    return (
      <div className="container" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div className="card text-center animate-slide-up" style={{ width: '100%' }}>
          <div style={{ color: 'var(--success)', marginBottom: '1.5rem', display: 'flex', justifyContent: 'center' }}>
            <CheckCircle size={64} />
          </div>
          <h2>¡Registro Exitoso!</h2>
          <p className="mt-4">El documento ha sido guardado correctamente.</p>
          <button className="btn btn-primary btn-full mt-6" onClick={resetForm}>
            Cargar Otro Registro
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container animate-fade-in" style={{ paddingBottom: '3rem' }}>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-gradient">Nuevo Registro</h2>
          <p>Driver: <strong>{driver.name}</strong></p>
        </div>
        <button className="btn btn-secondary" onClick={() => navigate('/')} style={{ padding: '0.5rem 1rem' }}>
          <ArrowLeft size={18} /> Salir
        </button>
      </div>

      <div className="card">
        {error && (
          <div style={{ background: 'hsla(350, 80%, 60%, 0.1)', color: 'var(--danger)', padding: '1rem', borderRadius: 'var(--radius-md)', marginBottom: '1.5rem', border: '1px solid hsla(350, 80%, 60%, 0.2)' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Base Fields */}
          <div className="form-group">
            <label className="form-label">Fecha</label>
            <input 
              type="date" 
              className="form-control" 
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Categoría del Documento</label>
            <select 
              className="form-control"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              required
            >
              <option value="" disabled>-- Selecciona una categoría --</option>
              <option value="remito">Remito (Carga/Descarga)</option>
              <option value="fuel">Gasto de Combustible</option>
              <option value="general">Gasto General</option>
            </select>
          </div>

          {/* Dynamic Fields */}
          <div className="animate-slide-up">
            {category === 'remito' && (
              <>
                <div className="form-group">
                  <label className="form-label">Lugar de Carga</label>
                  <input type="text" className="form-control" required value={loadingLocation} onChange={e => setLoadingLocation(e.target.value)} />
                </div>
                <div className="form-group">
                  <label className="form-label">Destino</label>
                  <input type="text" className="form-control" required value={destination} onChange={e => setDestination(e.target.value)} />
                </div>
                <div className="form-group">
                  <label className="form-label">Empresa</label>
                  <input type="text" className="form-control" required value={company} onChange={e => setCompany(e.target.value)} />
                </div>
                <div className="form-group">
                  <label className="form-label">Número de Remito</label>
                  <input type="text" className="form-control" required value={remitoNumber} onChange={e => setRemitoNumber(e.target.value)} />
                </div>
              </>
            )}

            {category === 'fuel' && (
              <div className="form-group">
                <label className="form-label">Litros Cargados</label>
                <input type="number" step="0.01" min="0" className="form-control" required value={liters} onChange={e => setLiters(e.target.value)} placeholder="Ej: 50.5" />
              </div>
            )}

            {category === 'general' && (
              <div className="form-group">
                <label className="form-label">Importe del Gasto ($)</label>
                <input type="number" step="0.01" min="0" className="form-control" required value={amount} onChange={e => setAmount(e.target.value)} placeholder="Ej: 1500" />
              </div>
            )}
          </div>

          {/* Photo Upload (Only show if category is selected) */}
          {category && (
            <div className="form-group mt-6 animate-slide-up">
              <label className="form-label">Fotografías del Comprobante (Máx. 2)</label>
              
              {photos.length < 2 && (
                <div 
                  className="photo-upload-area"
                  onClick={() => fileInputRef.current?.click()}
                >
                  <div style={{ color: 'var(--primary)', display: 'flex', gap: '1rem' }}>
                    <Camera size={32} />
                    <Upload size={32} />
                  </div>
                  <p style={{ margin: 0 }}>Toca aquí para tomar foto o elegir archivo</p>
                  <input 
                    type="file" 
                    accept="image/*" 
                    capture="environment" // Suggests mobile devices to open the camera
                    multiple
                    style={{ display: 'none' }}
                    ref={fileInputRef}
                    onChange={handlePhotoSelect}
                  />
                </div>
              )}

              {photos.length > 0 && (
                <div className="photo-preview-grid">
                  {photos.map((photo, index) => (
                    <div key={index} className="photo-preview-item animate-fade-in">
                      <img src={photo.preview} alt={`Preview ${index + 1}`} />
                      <button type="button" className="photo-remove-btn" onClick={() => removePhoto(index)}>
                        <X size={16} />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          <button 
            type="submit" 
            className="btn btn-primary btn-full mt-6"
            disabled={isSubmitting || !category || photos.length === 0}
          >
            {isSubmitting ? 'Enviando...' : 'Enviar Registro'}
          </button>
        </form>
      </div>
    </div>
  );
}
