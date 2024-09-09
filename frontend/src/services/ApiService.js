// ApiService.js
import axios from 'axios';

// Add backend URL here
baseUrl = 'http://128.189.222.53:8000';

class ApiService {
    static async getParkingData(currentLocation, range) {
      try {
        const response = await axios.post(`${baseUrl}/parkingData`, {
          "latitude" : currentLocation.latitude,
          "longitude" : currentLocation.longitude,
          "range" : range,
        });
        print(response.data);
        return response.data;
      } catch (error) {
        console.error('Error fetching parking data:', error);
        throw error;
      }
    }
  }
  
export default ApiService;