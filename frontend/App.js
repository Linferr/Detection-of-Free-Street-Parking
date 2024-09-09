// App.js
import React from 'react';
import MapScreen from './src/screens/MapScreen';
import TitleScreen from './src/screens/TitleScreen';
import {NavigationContainer} from '@react-navigation/native';
import MyStack from './Stack';

const App = () => {
  return (
    <NavigationContainer>
      <MyStack />
    </NavigationContainer>
  );
};

export default App;