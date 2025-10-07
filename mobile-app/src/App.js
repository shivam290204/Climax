// [file name]: App.js - ENHANCED
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from './screens/HomeScreen';
import MapScreen from './screens/MapScreen';
import HealthScreen from './screens/HealthScreen';
import 'react-native-gesture-handler';
const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} options={{ title: 'Air Quality Intelligence' }} />
        <Stack.Screen name="Map" component={MapScreen} options={{ title: 'Pollution Map' }} />
        <Stack.Screen name="Health" component={HealthScreen} options={{ title: 'Health Guidance' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}