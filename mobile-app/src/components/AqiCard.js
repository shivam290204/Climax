// [file name]: AqiCard.js - ENHANCED
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

function categoryColor(category) {
  switch (category) {
    case 'Good': return '#009966';
    case 'Satisfactory': return '#79bc6a';
    case 'Moderate': return '#ffde33';
    case 'Poor': return '#ff9933';
    case 'Very Poor': return '#cc0033';
    case 'Severe': return '#660099';
    default: return '#555';
  }
}

export default function AqiCard({ aqi, category, timestamp, sourceBreakdown }) {
  return (
    <View style={[styles.card, { borderColor: categoryColor(category) }]}>
      <Text style={styles.title}>Current AQI</Text>
      <Text style={[styles.aqi, { color: categoryColor(category) }]}>{aqi}</Text>
      <Text style={styles.category}>{category}</Text>
      
      {/* Source Attribution */}
      {sourceBreakdown && (
        <View style={styles.sourceContainer}>
          <Text style={styles.sourceTitle}>Pollution Sources:</Text>
          {Object.entries(sourceBreakdown).map(([source, percentage]) => (
            <View key={source} style={styles.sourceRow}>
              <View style={styles.sourceBarContainer}>
                <View 
                  style={[
                    styles.sourceBar, 
                    { width: `${percentage}%`, backgroundColor: getSourceColor(source) }
                  ]} 
                />
              </View>
              <Text style={styles.sourceText}>{source}: {percentage}%</Text>
            </View>
          ))}
        </View>
      )}
      
      <Text style={styles.time}>{new Date(timestamp).toLocaleTimeString()}</Text>
    </View>
  );
}

function getSourceColor(source) {
  const colors = {
    'Stubble Burning': '#8B4513',
    'Traffic': '#FF6B35',
    'Industry': '#4A90E2',
    'Construction': '#F9A825',
    'Other': '#9E9E9E'
  };
  return colors[source] || '#555';
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: '#fff',
    borderWidth: 2,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 4,
    elevation: 3,
    marginVertical: 12,
  },
  title: { fontSize: 16, fontWeight: '600', marginBottom: 4 },
  aqi: { fontSize: 48, fontWeight: '700' },
  category: { fontSize: 18, fontWeight: '500', marginTop: 4 },
  time: { fontSize: 12, color: '#777', marginTop: 8 },
  sourceContainer: { marginTop: 12 },
  sourceTitle: { fontSize: 14, fontWeight: '600', marginBottom: 8 },
  sourceRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 4 },
  sourceBarContainer: { 
    width: 60, 
    height: 8, 
    backgroundColor: '#f0f0f0', 
    borderRadius: 4, 
    marginRight: 8,
    overflow: 'hidden'
  },
  sourceBar: { height: '100%', borderRadius: 4 },
  sourceText: { fontSize: 12, color: '#555', flex: 1 }
});