import { Component, OnInit } from '@angular/core';
import { environment } from '../environments/environment.prod';
import { Map } from 'mapbox-gl';
import * as Mapboxgl from 'mapbox-gl';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent implements OnInit {

  opened = false;

  toggleSidebar(){
    this.opened = !this.opened;
  }

  ngOnInit() {

    var mapa = new Map({
      accessToken: environment.mapboxKey,
      container: 'mapa-mapbox',
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [-105.4821014,39.0233602], // LONG, LAT
      zoom: 6.55
    });

    this.createRSUmarker(mapa, "<b>Unit No. 1</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -106.47159, 39.620090)
    this.createRSUmarker(mapa, "<b>Unit No. 8</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -106.35329, 39.642160)
    this.createRSUmarker(mapa, "<b>Unit No. 11</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -106.27894, 39.621330)
    this.createRSUmarker(mapa, "<b>Unit No. 28</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -106.11322, 39.573120)
    this.createRSUmarker(mapa, "<b>Unit No. 38</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -106.01213, 39.652980)
    this.createRSUmarker(mapa, "<b>Unit No. 45</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -105.89362, 39.681830)
    this.createRSUmarker(mapa, "<b>Unit No. 55</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -105.76786, 39.696270)
    this.createRSUmarker(mapa, "<b>Unit No. 63</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -105.68687, 39.737630)
    this.createRSUmarker(mapa, "<b>Unit No. 70</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -105.59896, 39.764340)
    this.createRSUmarker(mapa, "<b>Unit No. 85</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -105.41536, 39.722900)
    this.createRSUmarker(mapa, "<b>Unit No. 90</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -105.33902, 39.702260)
    this.createRSUmarker(mapa, "<b>Unit No. 100</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -105.19113, 39.716260)
    this.createRSUmarker(mapa, "<b>Unit No. 117</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -105.084433, 39.553997)
    this.createRSUmarker(mapa, "<b>Unit No. 125</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -105.020854, 39.563273)
    this.createRSUmarker(mapa, "<b>Unit No. 144</b><br>Vehicle Count: n/a<br>IPv4 Status: 1.00<br>IPv6 Status: 1.00", -104.917766, 39.564718)

  }

  // function plots RSU markers as desired
  createRSUmarker(map: Map, popup: string, lng: number, lat: number){
    const marker = new Mapboxgl.Marker({
      draggable: false
      })
      .setLngLat([lng,lat])
      .setPopup(new Mapboxgl.Popup().setHTML(popup))
      .addTo(map);
  }

}
