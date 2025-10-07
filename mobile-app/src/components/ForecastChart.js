// [NEW FILE]: ForecastChart.js
import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';

const { width: screenWidth } = Dimensions.get('window');

export default function ForecastChart({ forecast }) {
  if (!forecast || forecast.length === 0) {
    return <Text style={styles.noData}>No forecast data available</Text>;
  }

  const maxAqi = Math.max(...forecast.map(f => f.aqi));
  const chartHeight = 150;

  return (
    <View style={styles.container}>
      <View style={styles.chart}>
        {forecast.slice(0, 9).map((hour, index) => {
          const barHeight = (hour.aqi / maxAqi) * chartHeight;
          return (
            <View key={index} style={styles.barContainer}>
              <View style={[styles.bar, { height: barHeight }]} />
              <Text style={styles.timeLabel}>
                {new Date(hour.time).getHours()}h
              </Text>
              <Text style={styles.aqiLabel}>{hour.aqi}</Text>
            </View>
          );
        })}
      </View>
      
      <View style={styles.legend}>
        <Text style={styles.legendText}>Next 24 hours forecast</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8
  },
  chart: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    height: 150,
    paddingHorizontal: 8
  },
  barContainer: {
    alignItems: 'center',
    flex: 1
  },
  bar: {
    width: 12,
    backgroundColor: '#007aff',
    borderRadius: 6,
    marginBottom: 4
  },
  timeLabel: {
    fontSize: 10,
    color: '#666',
    marginTop: 4
  },
  aqiLabel: {
    fontSize: 10,
    fontWeight: '600',
    color: '#333'
  },
  legend: {
    marginTop: 12,
    alignItems: 'center'
  },
  legendText: {
    fontSize: 12,
    color: '#666',
    fontStyle: 'italic'
  },
  noData: {
    textAlign: 'center',
    color: '#666',
    fontStyle: 'italic',
    marginVertical: 20
  }
});