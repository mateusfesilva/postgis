import React, { useState, useEffect } from 'react';
import {MapContainer, TileLayer} from 'react-leaflet';
import { useMap, Marker, Polygon, GeoJSON, Popup } from 'react-leaflet';
import { geoService } from '../services/geoService';
import 'leaflet/dist/leaflet.css';
import {map} from 'leaflet';
import "@geoman-io/leaflet-geoman-free";
import "@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css";

function MapView(){
    const [points, setPoints] = useState([]);
    const [polygons, setPolygons] = useState([]);

    useEffect(() => {
        loadMapData();
    }, []);

    const loadMapData = async () => {
        try {
            const pointResponse = await geoService.getPoints();
            const polygonResponse = await geoService.getPolygons();

            setPoints(pointResponse.data)
            setPolygons(polygonResponse.data)
        }catch (err){
            console.log('Error loading map data:', err);
        }
    };

    const [isReady, setIsReady] = useState(false);
    
    useEffect(() => {
        const timer = setTimeout(() => {
            setIsReady(true);
        }, 500);
        return () => clearTimeout(timer);
    }, []);

    return(
        <MapContainer center={[-23.55052, -46.633308]} zoom={13} style={{height: '100vh', width: '100%'}}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />

            <DrawingControls />

            {points && Array.isArray(points) && points.length > 0 && isReady && points.map(p => {
                return <Marker key={p.id} position={[p.coordinates[1], p.coordinates[0]]}>
                          <Popup>
                            {p.coordinates[1]}, {p.coordinates[0]}: {p.description}
                        </Popup>
                </Marker>;
            })}

            {polygons && Array.isArray(polygons) && polygons.length > 0 && polygons.map(poly => (
                console.log('Polygon JSON:', poly),
                <GeoJSON key={poly.id} data={poly.geometry}>
                    <Popup>
                        {poly.name}: {poly.category}
                    </Popup>
                </GeoJSON>
            ))}
        </MapContainer>
    );
}

export { MapView };

function DrawingControls() {
    const map = useMap();

    useEffect(() => {
        if (!map) return;

        map.pm.addControls({
            position: 'topleft',
            drawMarker: true,
            drawPolygon: true,
            drawPolyline: true,
            editMode: true,
            removalMode: true,
        });

        const onCreate = (e) => {
            if (!e || !e.layer) {
                console.warn('No layer found in event:', e);
                return;
            }
            const layer = e.layer;
            const shape = layer.toGeoJSON();
            handleSaveGeometry(shape);
        };

        map.on('pm:create', onCreate);

        return () => {
            map.off('pm:create', onCreate);
        };
    }, [map]);

    const handleSaveGeometry = async (shape) => {
        try {
            if (shape.geometry.type === 'Point') {
                await geoService.createPoint({
                    name: 'New Point',
                    description: 'Created from map',
                    geometry: shape.geometry,
                });
            } else if (shape.geometry.type === 'Polygon') {
                await geoService.createPolygon({
                    name: 'New Polygon',
                    category: 'Uncategorized',
                    geometry: shape.geometry,
                });
            }
            alert('Geometry saved successfully!');
        } catch (err) {
            console.error('Error saving geometry:', err);
            alert('Failed to save geometry.');
        }
    };

    return null;
}