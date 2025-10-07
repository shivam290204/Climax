// AQI category helpers and color mapping
export const AQI_CATEGORIES = [
  { name: 'Good', max: 50, color: '#009966' },
  { name: 'Satisfactory', max: 100, color: '#79bc6a' },
  { name: 'Moderate', max: 200, color: '#ffde33' },
  { name: 'Poor', max: 300, color: '#ff9933' },
  { name: 'Very Poor', max: 400, color: '#cc0033' },
  { name: 'Severe', max: 500, color: '#660099' }
];

export function categoryForAqi(aqi) {
  if (aqi == null) return 'Unknown';
  return (AQI_CATEGORIES.find(c => aqi <= c.max) || { name: 'Severe' }).name;
}

export function colorForCategory(category) {
  return AQI_CATEGORIES.find(c => c.name === category)?.color || '#555';
}
