// Must be first for React Navigation gesture support
import 'react-native-gesture-handler';
import { registerRootComponent } from 'expo';
import App from './src/App';

registerRootComponent(App);