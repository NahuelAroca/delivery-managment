const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const fetchDrivers = async () => {
  // In a real app we would have a /drivers endpoint.
  // Since we only seeded them, let's just hardcode the 4 drivers or fetch from a new endpoint if we had one.
  // Wait, did I create a GET /drivers endpoint? No, the requirements didn't specify one, 
  // but let's mock it for the UI, or we can just return static for now as per requirement:
  // "Pantalla para que el driver seleccione su nombre de una lista desplegable"
  return [
    { id: 1, name: "Driver 1" },
    { id: 2, name: "Driver 2" },
    { id: 3, name: "Driver 3" },
    { id: 4, name: "Driver 4" }
  ];
};

export const createRecord = async (formData) => {
  const response = await fetch(`${API_URL}/records/`, {
    method: 'POST',
    body: formData, // FormData automatically sets multipart/form-data
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error creating record');
  }
  
  return response.json();
};

export const fetchRecords = async (filters = {}) => {
  // Build query string
  const query = new URLSearchParams();
  if (filters.driver_id) query.append('driver_id', filters.driver_id);
  if (filters.category) query.append('category', filters.category);
  if (filters.start_date) query.append('start_date', filters.start_date);
  if (filters.end_date) query.append('end_date', filters.end_date);
  
  const response = await fetch(`${API_URL}/records/?${query.toString()}`);
  if (!response.ok) throw new Error('Error fetching records');
  return response.json();
};

export const fetchRecordDetail = async (id) => {
  const response = await fetch(`${API_URL}/records/${id}`);
  if (!response.ok) throw new Error('Error fetching record detail');
  return response.json();
};

