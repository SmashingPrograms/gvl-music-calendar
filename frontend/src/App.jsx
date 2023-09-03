import React, { useState, useEffect } from "react";
import Events from "./components/Events";

function App() {
  const [data, setData] = useState(null);

  const apiUrl = "http://localhost:5000/api";

  useEffect(() => {
    // Make a GET request to the backend API
    fetch(apiUrl)
      .then((response) => response.json())
      .then((responseData) => {
        // Set the received data in the state
        setData(responseData);
        console.log(responseData);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []); // The empty dependency array ensures this effect runs once on component mount


  return (
    <div className="App">
      <h1>Data from Backend:</h1>
      {data !== null ? (
        <>
          <Events data={data} /> 
        </>
      ) : (
        <p>Loading data...</p>
      )}
    </div>
  );
};

export default App;