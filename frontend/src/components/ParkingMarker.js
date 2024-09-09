// ParkingMarker.js
import React from 'react';
import { Marker } from 'react-native-maps';

const ParkingMarker = ({ coordinate, title }) => {
  return (
    <Marker
      coordinate={coordinate}
      title={title}>
        <Image
            source={require('../../assets/parking.png')}
            style={{ width: 30, height: 30 }}
        />
    </Marker>
  );
};

export default ParkingMarker;