import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, TouchableHighlight } from 'react-native';
import * as Location from 'expo-location';
import ApiService from '../services/ApiService';
import MapComponent from '../components/MapComponent';
import { TextInput } from 'react-native';

const MapScreen = ({navigation, route}) => {
    const [currentLocation, setCurrentLocation] = useState(null);
    const [initialRegion, setInitialRegion] = useState(null);
    const [markers, setMarkers] = useState([]);

    const addMarker = (coordinates) => {
      const newMarkers = coordinates.map(({ latitude, longitude }) => ({
        latitude,
        longitude,
      }));
      setMarkers(newMarkers) // Should clear all old markers
    };  

    const fetchData = async (range=3) => {
      console.log('Fetching data')
      if (!currentLocation) {
        console.log('Current location not available yet');
        return;
      }

      try {
        console.log("Fetching parking data")
        const data = await ApiService.getParkingData(currentLocation, range);
        addMarker(data);
      } 
      
      catch (error) {
        // Handle error
        console.error('Error fetching parking data:', error);
        throw error;
      }
    };

    useEffect(() => {
      const getLocation = async () => {
        let { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') {
          console.log('Permission to access location was denied');
          return;
        }
    
        let location = await Location.getCurrentPositionAsync({});
        setCurrentLocation(location.coords);
    
        setInitialRegion({
          latitude: location.coords.latitude,
          longitude: location.coords.longitude,
          latitudeDelta: 0.005,
          longitudeDelta: 0.005,
        });
    
        // Function to fetch location
        const fetchLocation = async () => {
          let newLocation = await Location.getCurrentPositionAsync({});
          setCurrentLocation(newLocation.coords);
        };
    
        // Fetch location initially
        fetchLocation();
    
        // Set interval to fetch location every second (1000 milliseconds)
        const locationInterval = setInterval(fetchLocation, 1000);
    
        // Set interval to fetch data every 3 minutes (180000 milliseconds)
        const dataInterval = setInterval(fetchData, 180000);
    
        // Cleanup function to clear intervals when component unmounts
        return () => {
          clearInterval(locationInterval);
          clearInterval(dataInterval);
        };
      };
    
      getLocation();
    
    }, []);
  
    return (
        <View style={styles.container}>
          {initialRegion && (
            <MapComponent
              currentLocation={currentLocation}
              initialRegion={initialRegion}
              markers={markers}
            />
          )}

          <View style={styles.distanceButtonContainer}>
          <TouchableOpacity style={styles.button} onPress={() => fetchData(0.5)}>
            <Text style={styles.buttonText}>500 m</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={() => fetchData(1)}>
            <Text style={styles.buttonText}>1 km</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={() => fetchData(3)}>
            <Text style={styles.buttonText}>3 km</Text>
          </TouchableOpacity>
        </View>
        <StatusBar style="auto" />
      </View>
    );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    backgroundColor: '#007AFF',
    paddingVertical: 12,
    paddingHorizontal: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#007AFF', // Same as background color for consistency
    marginVertical: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  distanceButtonContainer: {
    position: 'absolute',
    bottom: 20,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between',
  }
});

export default MapScreen;
