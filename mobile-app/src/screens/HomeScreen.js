// [file name]: HomeScreen.js - ENHANCED
import React from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Button, ScrollView, TouchableOpacity } from 'react-native';
import { useAqi } from '../hooks/useAqi';
import AqiCard from '../components/AqiCard';
import HealthRecommendations from '../components/HealthRecommendations';
import ForecastChart from '../components/ForecastChart';
import { colorForCategory } from '../../../shared/src/aqiCategories';

export default function HomeScreen({ navigation }) {
  const { data, loading, error, refresh } = useAqi();

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.headerRow}>
        <Text style={styles.header}>Air Quality Intelligence</Text>
        <TouchableOpacity 
          style={styles.mapButton}
          onPress={() => navigation.navigate('Map')}
        >
          <Text style={styles.mapButtonText}>Map</Text>
        </TouchableOpacity>
      </View>
      
      {loading && <ActivityIndicator size="large" color="#007aff" />}
      {error && <Text style={styles.error}>Error: {error}</Text>}
      
      {data && (
        <>
          <AqiCard 
            aqi={data.current_aqi} 
            category={data.current_category} 
            timestamp={data.timestamp}
            sourceBreakdown={data.source_breakdown}
          />
          
          <HealthRecommendations 
            recommendations={data.health_recommendations}
            aqi={data.current_aqi}
            category={data.current_category}
          />
          
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>72-Hour Forecast</Text>
            <ForecastChart forecast={data.extended_forecast} />
          </View>
          
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Next 6 Hours</Text>
            {data.hourly_forecast.slice(0,6).map((h, idx) => (
              <View key={idx} style={styles.hourRow}>
                <Text style={styles.hourTime}>{new Date(h.time).getHours()}:00</Text>
                <Text style={styles.hourAqi}>AQI {h.aqi}</Text>
                <Text style={[styles.hourCategory, {color: colorForCategory(h.category)}]}>
                  {h.category}
                </Text>
              </View>
            ))}
          </View>
        </>
      )}
      
      <Button title="Refresh Data" onPress={refresh} color="#007aff" />
    </ScrollView>
  );
}

// category color now imported from shared

const styles = StyleSheet.create({
  container: { padding: 20, backgroundColor: '#f5f7fa' },
  headerRow: { 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center',
    marginBottom: 12 
  },
  header: { fontSize: 24, fontWeight: '700' },
  mapButton: { 
    backgroundColor: '#007aff', 
    paddingHorizontal: 16, 
    paddingVertical: 8, 
    borderRadius: 8 
  },
  mapButtonText: { color: 'white', fontWeight: '600' },
  error: { color: 'red', marginVertical: 8 },
  section: { 
    marginTop: 24, 
    backgroundColor: 'white', 
    padding: 16, 
    borderRadius: 12,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 4,
    elevation: 2,
  },
  sectionTitle: { fontSize: 18, fontWeight: '600', marginBottom: 12 },
  hourRow: { 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0'
  },
  hourTime: { fontSize: 14, fontWeight: '500', width: 60 },
  hourAqi: { fontSize: 14, fontWeight: '600', flex: 1 },
  hourCategory: { fontSize: 12, fontWeight: '500' }
});