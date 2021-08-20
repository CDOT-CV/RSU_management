import React from "react"

function RsuMarker(props) {
  var circleStyle = {
    padding:5,
    display:"inline-block",
    backgroundColor: (props.onlineStatus === "online" ? '#A1D363' : '#E94F37'),
    borderRadius: "50%",
    width:5,
    height:5,
  };
  
  return (
    <div style={circleStyle}>
    </div>
  );
}

export default RsuMarker;