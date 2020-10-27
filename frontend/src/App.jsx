import React, { Component } from "react";

const App = () => {
  const evtSource = new EventSource("http://localhost/histoday/ml/BTC/train");
  evtSource.addEventListener("status", function(event) {
      // Logic to handle status updates
      console.log(event)
  });
  evtSource.addEventListener("end", function(event) {
      console.log(event)
      evtSource.close();
  });
  return (
    <div style={{ textAlign: "center" }}>
       <p>Loading...</p>}
    </div>
  )
};

export default App;