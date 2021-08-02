import React, { useEffect, useState } from "react"
import ReactMapGL, { Marker, Popup } from "react-map-gl"
import RsuMarker from './RsuMarker';
import Header from './Header';

const axios = require('axios').default;

const REACT_APP_MAPBOX_TOKEN = "pk.eyJ1IjoiZHJld2pqIiwiYSI6ImNrcWtqMGU5YzNlNDgycGxjNmw0NWQ0eGsifQ.jMxZO_Qs38YyYc137cNCew";

function Map(props) {
  const [viewport, setViewport] = useState({
    latitude: 39.7392,
    longitude: -104.9903,
    width: '100%',
    height: '100vh',
    zoom: 10
  });

  const [selectedRsu, setSelectedRsu] = useState(null);

  const [selectedRsuCount, setSelectedRsuCount] = useState(null);

  const getRsuData = ((rsuIp) => {
    try {
      let response = axios.get('https://rsu-manager-apigateway-5xm3e3o5.uc.gateway.dev/rsucounts/' + rsuIp);
      response.then(function(result) { setSelectedRsuCount(result.data.count) });
    } catch (error) {
      console.log(error);
    }
  });

  useEffect(() => {
    const listener = e => {
      if (e.key === "Escape")
        setSelectedRsu(null);
    };
    window.addEventListener("keydown", listener);
    
    return () => {
      window.removeEventListener("keydown", listener);
    }
  }, []);

  return (
    <div>
      <ReactMapGL 
        {...viewport} 
        mapboxApiAccessToken={REACT_APP_MAPBOX_TOKEN}
        mapStyle="mapbox://styles/drewjj/ckr1p5ulb4uys18quax950ia4"
        onViewportChange={(viewport) => {
          setViewport(viewport);
        }}>
          <Header/>

          {props.rsuData.map((rsu) => (
            <Marker 
              key={rsu.id} 
              latitude={rsu.geometry.coordinates[1]} 
              longitude={rsu.geometry.coordinates[0]}>

              <button 
                class="marker-btn" 
                onClick={(e) => {
                e.preventDefault();
                setSelectedRsuCount(null);
                setSelectedRsu(rsu);
                getRsuData(rsu.properties.Ipv4Address);
              }}>
                <RsuMarker onlineStatus={rsu.onlineStatus}/>
              </button>

            </Marker>
          ))}

          {selectedRsu ? (
            <Popup
              latitude={selectedRsu.geometry.coordinates[1]} 
              longitude={selectedRsu.geometry.coordinates[0]}
              onClose={() => {
                setSelectedRsu(null);
                setSelectedRsuCount(null);
              }}>

              <div>
                <h2 class="popop-h2">{selectedRsu.properties.Ipv4Address}</h2>
                <p class="popop-p">Online Status: {selectedRsu.onlineStatus}</p>
                <p class="popop-p">Milepost: {selectedRsu.properties.Milepost}</p>
                <p class="popop-p">
                  Serial Number: {selectedRsu.properties.SerialNumber ? 
                  selectedRsu.properties.SerialNumber : 'Unknown'}
                </p>
                <p class="popop-p">BSM Counts: {selectedRsuCount}</p>
              </div>

            </Popup>
          ) : null}
          
      </ReactMapGL>
    </div>
  );
}

export default Map;