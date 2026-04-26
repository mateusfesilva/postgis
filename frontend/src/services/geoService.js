import api from './api';

export const geoService = {
    getPoints: () => api.get('/points/'),
    createPoint: (pointData) => api.post('/points/', pointData),
    deletePoint: (id) => api.delete(`/points/${id}/`),
    getPolygons: () => api.get('/polygons/'),
    createPolygon: (polygonData) => api.post('/polygons/', polygonData),
    deletePolygon: (id) => api.delete(`/polygons/${id}/`),
};