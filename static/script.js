const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let stars = [];
for (let i = 0; i < 100; i++) {
    stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 2,
        speed: Math.random() * 0.5
    });
}

function drawStars() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < stars.length; i++) {
        ctx.beginPath();
        ctx.arc(stars[i].x, stars[i].y, stars[i].radius, 0, 2 * Math.PI);
        ctx.fillStyle = '#fff';
        ctx.fill();
        stars[i].x -= stars[i].speed;
        if (stars[i].x < 0) {
            stars[i].x = canvas.width;
            stars[i].y = Math.random() * canvas.height;
        }
    }
    requestAnimationFrame(drawStars);
}

drawStars();

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const fullName = document.getElementById('fullName').value;

    try {
        const response = await fetch('/api/v1/users/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                password,
                fullName
            })
        });
        const data = await response.json();
        if (data.message === 'User registered successfully') {
            alert('Registration successful!');
        } else {
            document.getElementById('error-message').innerText = data.message;
        }
    } catch (error) {
        console.error(error);
    }
});