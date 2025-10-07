// [NEW FILE]: src/screens/MapScreen.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function MapScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Pollution Map</Text>
      <Text style={styles.comingSoon}>Map View Coming Soon</Text>
      <Text style={styles.description}>
        This will show a heat map of pollution levels across Delhi-NCR
        with real-time source attribution data.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f7fa',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    marginBottom: 20,
  },
  comingSoon: {
    fontSize: 18,
    color: '#007aff',
    marginBottom: 16,
    fontWeight: '600',
  },
  description: {
    fontSize: 16,
    textAlign: 'center',
    color: '#666',
    lineHeight: 24,
  },
});