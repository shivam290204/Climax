// [NEW FILE]: HealthRecommendations.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function HealthRecommendations({ recommendations, aqi, category }) {
  const getGeneralRecommendations = () => {
    if (aqi <= 50) return "Air quality is satisfactory. Enjoy outdoor activities.";
    if (aqi <= 100) return "Air quality is acceptable. Unusually sensitive people should consider reducing prolonged outdoor exertion.";
    if (aqi <= 200) return "Members of sensitive groups may experience health effects. General public is less likely to be affected.";
    if (aqi <= 300) return "Health alert: everyone may begin to experience health effects.";
    if (aqi <= 400) return "Health warning of emergency conditions. The entire population is more likely to be affected.";
    return "Health emergency: everyone may experience more serious health effects.";
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Health Recommendations</Text>
      <Text style={styles.generalRecommendation}>{getGeneralRecommendations()}</Text>
      
      {recommendations && recommendations.map((rec, index) => (
        <View key={index} style={styles.recommendationItem}>
          <Text style={styles.recommendationText}>• {rec}</Text>
        </View>
      ))}
      
      <View style={styles.tipsContainer}>
        <Text style={styles.tipsTitle}>Quick Tips:</Text>
        <Text style={styles.tip}>• Use N95 masks when outdoors</Text>
        <Text style={styles.tip}>• Avoid strenuous outdoor activities</Text>
        <Text style={styles.tip}>• Use air purifiers indoors</Text>
        <Text style={styles.tip}>• Keep windows closed during high pollution</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#e8f4fd',
    padding: 16,
    borderRadius: 12,
    marginVertical: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#007aff'
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 8,
    color: '#1a365d'
  },
  generalRecommendation: {
    fontSize: 14,
    marginBottom: 12,
    lineHeight: 20,
    color: '#2d3748'
  },
  recommendationItem: {
    marginBottom: 6
  },
  recommendationText: {
    fontSize: 14,
    lineHeight: 20,
    color: '#4a5568'
  },
  tipsContainer: {
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#cbd5e0'
  },
  tipsTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#1a365d'
  },
  tip: {
    fontSize: 13,
    marginBottom: 4,
    color: '#4a5568'
  }
});