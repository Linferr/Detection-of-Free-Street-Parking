import * as React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import TitleScreen from './src/screens/TitleScreen';
import MapScreen from './src/screens/MapScreen';

const Stack = createNativeStackNavigator();

const MyStack = () => {
  return (
    <Stack.Navigator>
    <Stack.Screen
        name="Park Scanner"
        component={TitleScreen}
    />
    <Stack.Screen name="Map" component={MapScreen} />
    </Stack.Navigator>
  );
};

export default MyStack;