// MapComponent.js
import React from 'react';
import { StyleSheet, Image } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import ParkingMarker from './ParkingMarker';

const MapComponent = ({ currentLocation, initialRegion, markers }) => {
  return (
    <MapView
      style={styles.map}
      initialRegion={initialRegion}>
        {currentLocation && (
            <Marker
                coordinate={{
                    latitude: currentLocation.latitude,
                    longitude: currentLocation.longitude,
                }}
                title="Your location">
                <Image
                    source={require('../../assets/location.png')}
                    style={{ width: 30, height: 30 }}
                />
            </Marker>
        )}

        {markers.map((marker, index) => (
            <Marker
                key={index}
                coordinate={{
                    latitude: marker.latitude,
                    longitude: marker.longitude,
                }}
                title="Parking Spot">
                <Image
                    source={require('../../assets/parking.png')}
                    style={{ width: 30, height: 30 }}
                />
            </Marker>
        ))}
    </MapView>
  );
};

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
    },
    map: {
      width: '100%',
      height: '100%',
    },
    floatingButtonContainer: {
      position: 'absolute',
      bottom: 16,
      right: 16,
    }
});

export default MapComponent;