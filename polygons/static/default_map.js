// Инициализируем карту
const MCS = [55.75, 37.62];
const SPB = [59.94, 30.32];
const map = L.map('map').setView(SPB, 11);

// Добавляем слой OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// Добавляем линию антимеридиана
var antimeridianLine = L.polyline([
    [90, 180], // Северный полюс
    [-90, 180] // Южный полюс
], {
    color: 'yellow', // цвет
    weight: 0.5, // толщина
}).addTo(map);