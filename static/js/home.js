import * as THREE from 'three';
import { CSS3DRenderer, CSS3DObject } from 'three/addons/renderers/CSS3DRenderer.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';


const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('tjs-container').append(renderer.domElement);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const controls = new OrbitControls(camera, renderer.domElement);
const loader = new GLTFLoader();

var globe;

const url = '/static/models/low_poly_earth/scene.gltf';
loader.load(url, (gltf) => {
    globe = gltf.scene;
    scene.add(globe);
});

const geometry = new THREE.ConeGeometry(0.03, 0.05, 5);
const material = new THREE.MeshStandardMaterial( { color: 0x00ff00 } );
const cube = new THREE.Mesh( geometry, material );
cube.position.set(0, -1.1, 0);
const group = new THREE.Group();
group.add(cube);
scene.add( group );

const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(3, 2, 5).normalize();
scene.add(light);
camera.position.z = 1.8;

function animate() {
    if (globe) {
        globe.rotation.y += 0.003;
    }
    group.rotation.x += 0.003;
    group.rotation.z += 0.004;
    renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);