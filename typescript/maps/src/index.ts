/// <reference path="./env.d.ts" />
import { Map } from './Map';
import { User } from './User';

const apiKey = process.env.GOOGLE_MAPS_API_KEY;
if (!apiKey) {
  throw new Error('Set GOOGLE_MAPS_API_KEY in maps/.env before starting Parcel.');
}

const mapsWindow = window as Window & { initMap?: () => void };
mapsWindow.initMap = () => {
  new Map('map').addUserMarker(new User());
};

const script = document.createElement('script');
script.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(apiKey)}&loading=async&callback=initMap`;
script.async = true;
script.onerror = () => console.error('Failed to load the Google Maps API.');
document.head.appendChild(script);
