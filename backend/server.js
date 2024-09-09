// Load HTTP module
const express = require("express");
const bodyParser = require("body-parser");
const { MongoClient, ServerApiVersion } = require("mongodb");
const uri = "mongodb+srv://frontendtest:testpassword@cluster0.vutwh2x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

const app = express();
const port = 8000;

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri, {
    serverApi: {
        version: ServerApiVersion.v1,
        strict: true,
        deprecationErrors: true,
    }
});

async function run() {
    try {
        // Connect the client to the server
        await client.connect();
        // Send a ping to confirm a successful connection
        await client.db("admin").command({ ping: 1 });        
        console.log("Connected to MongoDB");
    } catch (err) {
        console.error("Error connecting to MongoDB:", err);
        process.exit(1);
    }
}
run();

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// POST endpoint to handle /parkingData
app.post('/parkingData', async (req, res) => {
    // Extract latitude, longitude, and range from request body
    const { latitude, longitude, range } = req.body;

    // Log received data
    console.log('userLatitude:', latitude);
    console.log('userLongitude:', longitude);
    console.log('inputRange:', range);

    try {
        // Get database reference
        const db = client.db("demoDB");

        // Find nearby parking locations
        const coordinates = await db.collection("availableParking").find({
            location: {
                $near: {
                    $geometry: { type: "Point", coordinates: [parseFloat(longitude), parseFloat(latitude)] },
                    $maxDistance: parseInt(range*1000)
                }
            }
        }).toArray();

        // Format response
        const formattedCoordinates = coordinates.map(coord => {
            return { latitude: coord.location[1], longitude: coord.location[0] };
        });

        // Set response headers and send response
        res.status(200).json(formattedCoordinates);
    } catch (err) {
        console.error("Error retrieving data from MongoDB:", err);
        res.status(500).send("Internal Server Error");
    }
});

// Handle other routes
app.use((req, res) => {
    res.status(404).send("Not Found\n");
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
