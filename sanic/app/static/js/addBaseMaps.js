maps = [
  { name: "OSM standard",
    url:"https://tiles.wmflabs.org/osm/{z}/{x}/{y}.png",
    maxZoom: 19,
    apiKey: "" },
  { name: "OSM (en)",
    url: "https://tiles.wmflabs.org/osm-multilingual/en,_/{z}/{x}/{y}.png",
    maxZoom: 19,
    apiKey: ""
  },
  { name: "OSM (de)",
    url: "https://tiles.wmflabs.org/osm-multilingual/de,en,_/{z}/{x}/{y}.png",
    maxZoom: 19,
    apiKey: ""
  },
  { name: "OSM no labels",
    url:"https://tiles.wmflabs.org/osm-no-labels/{z}/{x}/{y}.png",
    maxZoom: 15,
    apiKey: ""},
  { name: "OSM black & white",
    url:"https://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png",
    maxZoom: 19,
    apiKey: ""
  },
  { name: "Hikebike",
    url:"https://tiles.wmflabs.org/hikebike/{z}/{x}/{y}.png",
    maxZoom: 20,
    apiKey: ""
  },
  { name: "Blue-marble",
    url:"http://s3.amazonaws.com/com.modestmaps.bluemarble/{z}-r{y}-c{x}.jpg",
    maxZoom: 10,
    apiKey: ""
  },
  { name: "Landoceanice",
    url:"file:///home/chy/dl/dnb_land_ocean_ice/{z}/{x}/{y}.2.png",
    maxZoom: 7,
   apiKey: ""
  },
  { name: "Sattelite",
    url:"http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    maxZoom: 18,
    apiKey: "",
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
  },
  { name: "Relief",
    url:"http://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}",
    maxZoom: 14,
    apiKey: ""
  },
  { name: "Physical",
    url:"http://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}",
    maxZoom: 9,
    apiKey: ""
  },
  { name: "OpenTopoMap",
    url: "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    apiKey: '',
    maxZoom: 17,
    attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
  },
  { name: "OpenStreetMap.France",
    url: "https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png",
    apiKey: '',
    maxZoom: 20,
    attribution: '&copy; Openstreetmap France | &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  },
  { name: "OpenMapSurfer.Roads",
    url: "https://maps.heigit.org/openmapsurfer/tiles/roads/webmercator/{z}/{x}/{y}.png",
    apiKey: '',
    maxZoom: 19,
    attribution: 'Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> | Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  },
  { name: "Hydda.Base",
    url: "https://{s}.tile.openstreetmap.se/hydda/base/{z}/{x}/{y}.png",
    apiKey: '',
    maxZoom: 18,
    attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  },
  { name: "Esri.WorldStreetMap",
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    apiKey: '',
    maxZoom: 18,
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
  },
  { name: "Esri.DelLorme",
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/Specialty/DeLorme_World_Base_Map/MapServer/tile/{z}/{y}/{x}",
    attribution: 'Tiles &copy; Esri &mdash; Copyright: &copy;2012 DeLorme',
    minZoom: 1,
    maxZoom: 11 
  },
  { name: "Esri.WorldTopoMap",
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
  },
  { name: "Esri.WorldTerrain",
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}",
    maxZoom: 13,
    attribution: 'Tiles &copy; Esri &mdash; Source: USGS, Esri, TANA, DeLorme, and NPS'
  },
  { name: "ViirsEarthAtNight2012",
	  url: "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/VIIRS_CityLights_2012/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.jpeg",
    attribution: 'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
    bounds: [[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
    minZoom: 1,
    maxZoom: 8,
    format: 'jpg',
    time: '',
    tilematrixset: 'GoogleMapsCompatible_Level' 
  },
  { name: "Esri.WorldShadeRelief",
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}",
    maxZoom: 13,
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri'
  }
];


// Variables
var baseMaps = {};

// Create TileLayers from maps
for (i = 0; i < maps.length; i++) {
  maps[i].layer = function() {
    l = new L.TileLayer(this.url, {
      maxZoom: this.maxZoom,
      apiKey: this.apiKey
    });
  return l;
  }
};

// Populate BaseMap object with layers
for (i = 0; i < maps.length; i++) {
  baseMaps[maps[i].name] = maps[i].layer();
};

// initialize the map on the "map" div with a given center and zoom
var map = new L.Map('map', {
  center: [50, 10],
  zoom: 5,
  minZoom: 1,
  zoomSnap: 0,
  boxZoom: true,
  crs: 	L.CRS.EPSG3857,
  keyboard: true,
  keyboardPanDelta: 80,
  maxBounds: [[-90, -180], [90, 180]]
});
console.log('Created map');

// Add default layer to map
map.addLayer(baseMaps["Sattelite"]);
console.log('Added Default Layer');

// Generate layer switch control
L.control.layers(baseMaps).addTo(map);
console.log('Added Layer Control');


