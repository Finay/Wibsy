import * as THREE from "three";
import {
  CSS3DRenderer,
  CSS3DObject,
} from "three/addons/renderers/CSS3DRenderer.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById("tjs-container").append(renderer.domElement);

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  100,
);
camera.position.set(-8, 0, 0);
const controls = new OrbitControls(camera, renderer.domElement);

scene.add(new THREE.AmbientLight(0xffffff, 0.3));
const light = new THREE.DirectionalLight(0xffffff, 2);
light.position.set(-8, 3, 7).normalize();
scene.add(light);

var globe_model,
  world_group = new THREE.Group();
scene.add(world_group);

const AVATAR_OFFSET = -4.35;
const convertCoords = (lat, lng) => [
  (lat / 180) * Math.PI + Math.PI / 2,
  (lng / 180) * Math.PI,
];

class Avatar {
  constructor(lat, lng, color = 0x00ff00) {
    this.lat = lat;
    this.lng = lng;
    const geometry = new THREE.ConeGeometry(0.1, 0.2, 3);
    const material = new THREE.MeshStandardMaterial({ color: color });
    this.model = new THREE.Mesh(geometry, material);
    this.model.position.set(0, AVATAR_OFFSET, 0);
    this.positioner = new THREE.Group();
    this.positioner.add(this.model);
    const coords = convertCoords(lat, lng);
    console.log(coords);
    this.positioner.rotation.z = coords[0];
    this.positioner.rotation.y = coords[1];
  }
}

const loader = new GLTFLoader();
const url = "/static/models/low_poly_earth_3/untitled.gltf";
loader.load(url, (gltf) => {
  globe_model = gltf.scene;
  world_group.add(globe_model);

  const tokyo = new Avatar(35.6764225, 139.650027);

  world_group.add(tokyo.positioner);

  function animate() {
    world_group.rotation.y += 0.003;
    renderer.render(scene, camera);
  }
  renderer.setAnimationLoop(animate);
});
