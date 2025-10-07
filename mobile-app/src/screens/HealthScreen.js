// [NEW FILE]: src/screens/HealthScreen.js
import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { HEALTH_GUIDELINES } from '../../../shared/src/healthGuidance';

export default function HealthScreen() {
  const healthGuidelines = HEALTH_GUIDELINES;

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Health Guidelines</Text>
      
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>AQI Health Recommendations</Text>
        {healthGuidelines.map((guideline, index) => (
          <View key={index} style={styles.guidelineCard}>
            <Text style={styles.aqiRange}>{guideline.range}</Text>
            <Text style={styles.advice}>{guideline.advice}</Text>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Protective Measures</Text>
        <View style={styles.tipsCard}>
          <Text style={styles.tip}>• Use N95/FFP2 masks when outdoors</Text>
          <Text style={styles.tip}>• Avoid strenuous outdoor activities during high pollution</Text>
          <Text style={styles.tip}>• Use air purifiers at home and office</Text>
          <Text style={styles.tip}>• Keep windows closed during peak pollution hours</Text>
          <Text style={styles.tip}>• Stay hydrated and maintain a healthy diet</Text>
          <Text style={styles.tip}>• Monitor air quality before planning outdoor activities</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>For Sensitive Groups</Text>
        <View style={styles.sensitiveCard}>
          <Text style={styles.warning}>
            Children, elderly, pregnant women, and people with pre-existing respiratory or cardiovascular conditions should take extra precautions.
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f7fa',
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    marginBottom: 20,
    textAlign: 'center',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
    color: '#1a365d',
  },
  guidelineCard: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 8,
    marginBottom: 8,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 1 },
    shadowRadius: 3,
    elevation: 2,
  },
  aqiRange: {
    fontSize: 16,
    fontWeight: '600',
    color: '#007aff',
    marginBottom: 4,
  },
  advice: {
    fontSize: 14,
    color: '#4a5568',
    lineHeight: 20,
  },
  tipsCard: {
    backgroundColor: '#e8f4fd',
    padding: 16,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#007aff',
  },
  tip: {
    fontSize: 14,
    color: '#2d3748',
    marginBottom: 8,
    lineHeight: 20,
  },
  sensitiveCard: {
    backgroundColor: '#fff5f5',
    padding: 16,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#e53e3e',
  },
  warning: {
    fontSize: 14,
    color: '#742a2a',
    lineHeight: 20,
    fontStyle: 'italic',
  },
});