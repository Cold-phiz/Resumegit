document.addEventListener('DOMContentLoaded', function () {
    var content = document.getElementById('content');

    // Listen for scroll event on the document
    document.addEventListener('scroll', function () {
        // Apply the scroll position to the content
        content.scrollTop = window.scrollY;
    });
});

// Get the canvas and its 2D drawing context
const canvas = document.getElementById("fireworkCanvas");
const ctx = canvas.getContext("2d");

// Set canvas size on resize
function setCanvasSize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

// Define firework properties
let gravity = 0.015;
let particleAmount = 150;
let particleSize = 5;
let particleFadeAway = 0.002;
let particleShrinkage = 0.03;
let explosionSize = 5;
let fireworkGenerationRate = 0.006;
const fireworks = [];

// Set canvas size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Call setCanvasSize initially and on window resize
setCanvasSize();
window.addEventListener('resize', setCanvasSize);

function createFirework() {
  const firework = {
    x: Math.floor(Math.random() * canvas.width), // Random x position within canvas width
    y: Math.floor(Math.random() * (canvas.height * 0.8)), // Random y position within top half of canvas
    vx: Math.random() - 0.5, // Random horizontal velocity (-0.5 to 0.5)
    vy: Math.random(), // Random vertical velocity
    color: [Math.random() * 255, Math.random() * 255, Math.random() * 255], // Random color as RGB array
    explosionSize: Math.random() * explosionSize + 3.5, // Random explosion size
    particles: [], // Array to store explosion particles
  };

  fireworks.push(firework);
}

// Function to explode a firework
function explodeFirework(firework) {
  // Generate explosion particles
  for (let i = 0; i < particleAmount; i++) {
    const angle = Math.random() * Math.PI * 2; // Random angle
    const speed = Math.random() * 2.5; // Random speed
    // Number of explosion particles
    const particle = {
      x: firework.x,
      y: firework.y,
      vx: Math.cos(angle) * speed, // Horizontal velocity based on angle
      vy: Math.sin(angle) * speed, // Vertical velocity based on angle
      color: firework.color, // Color from firework
      size: Math.random() * particleSize + 2, // Random particle size
      alpha: 1, // Initial opacity
    };

    firework.particles.push(particle);
  }
}

function update() {
  // Clear the canvas slightly
  ctx.fillStyle = "rgba(0, 0, 0, 0.3)"; 
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Update and draw each firework
  fireworks.forEach((firework, index) => {
    if (firework.particles.length === 0) {
      firework.x += firework.vx;
      firework.y += firework.vy;
      firework.vy += gravity;
    } else {
      // Update and draw explosion particles
      firework.particles.forEach((particle) => {
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.vy += gravity;

        // Decrease opacity gradually
        particle.alpha -= particleFadeAway;

        // Decrease size gradually
        particle.size -= particleShrinkage;

        // Set particle color with adjusted opacity
        ctx.beginPath();
        ctx.fillStyle = `rgba(${particle.color[0]}, ${particle.color[1]}, ${particle.color[2]}, ${particle.alpha})`; // Use rgba for color with alpha
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fill();
      });

      // Remove particles that have gone off the screen, faded away, or shrunk to a very small size
      firework.particles = firework.particles.filter(
        (particle) =>
          particle.alpha > 0 &&
          particle.y < canvas.height &&
          particle.x >= 0 &&
          particle.x <= canvas.width &&
          particle.size > 0.1
      );

      // Remove fireworks with no particles left
      if (firework.particles.length === 0) {
        fireworks.splice(index, 1);
      }
    }
  });

  // Check if any fireworks need to explode
  fireworks.forEach((firework) => {
    if (firework.vy >= 0 && firework.particles.length === 0) {
      explodeFirework(firework);
    }
  });

  // Generate new fireworks randomly
  if (Math.random() < fireworkGenerationRate) {
    // Adjust the frequency of firework generation
    createFirework();
  }

  requestAnimationFrame(update);
}

// Start the animation loop
update();
