import React, { Component } from "react";

const App = () => {
  const evtSource = new EventSource("http://localhost/BTC/train");
  evtSource.addEventListener("progress", function(event) {
      // Logic to handle status updates
      console.log(event)
  });
  evtSource.addEventListener("end", function(event) {
      console.log('Handling end....')
      evtSource.close();
  });
  return (
    <div style={{ textAlign: "center" }}>
       <p>Loading...</p>}
    </div>
  )
};

export default App;