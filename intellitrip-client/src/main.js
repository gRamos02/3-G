import axios from 'axios';
const baseUrl = "http://localhost:8000";
const backgrounds = [
    'https://humanidades.com/wp-content/uploads/2017/03/ciudad-3-e1565900111723.jpg',
    'https://www.bancomundial.org/content/dam/photos/780x439/2018/oct-3/BuenosAires780.jpg',
    'https://cdn.forbes.com.mx/2023/02/ciudades-mas-visitadas-2023.webp',
];


function changeBackgroundAutomatically() {
    const randomIndex = Math.floor(Math.random() * backgrounds.length);
    const selectedBackground = backgrounds[randomIndex];
    const backgroundDiv = document.getElementById('backgroundDiv');
    backgroundDiv.style.backgroundImage = `url(${selectedBackground})`;
}

setInterval(changeBackgroundAutomatically, 5000);

changeBackgroundAutomatically();

async function cambiarOpacidad() {
    const input = document.querySelector('#message').value;
    const info = document.getElementById('info');

    try {
        const response = await fetch(`${baseUrl}/consulta?input=${input}`);

        if (response.status === 200) {
            const data = await response.json();

            
            document.querySelector("#title").innerHTML = data.city;
            document.querySelector("#description").innerHTML = data.description;

            info.style.opacity = '0.8'; // You may want to update this based on your data
        } else {
            console.error('Failed to fetch data. Status code:', response.status);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

const boton = document.getElementById('onclick');
boton.addEventListener('click', cambiarOpacidad);



