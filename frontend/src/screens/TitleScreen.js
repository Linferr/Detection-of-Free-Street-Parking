import * as React from 'react';
import { Button, Image, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack'; 

const TitleScreen = ({navigation}) => {
    const handleStart = () => {
        if (navigation) {
            navigation.navigate('Map');
        }
    };

    return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: 'white' }}>
            <Image
                source={require('../../assets/logo.png')}
                style={{ width: 500, height: 500 }} // Adjusted width and height
            />
            <View style={{ borderWidth: 2, borderColor: 'black', borderRadius: 10, padding: 10 }}>
                <Button title="Start" onPress={handleStart} color="black" />
            </View>
        </View>
    );
};

export default TitleScreen;
