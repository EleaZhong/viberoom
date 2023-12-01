// p5.js script for visualizing sentiment data

/*
let sentimentScore;
let sentimentMagnitude;

let ellipses = [];

function setup() {
  createCanvas(windowWidth, windowHeight);
  background(0);
  frameRate(10); // Limit the frame rate to prevent excessive querying

  // Create multiple ellipses
  for (let i = 0; i < 25; i++) {
    ellipses.push({
      locx: random(windowWidth),
      locy: random(windowHeight),
      size: random(4, 100)
    });
  }
}

function draw() {
  // Query the server for the latest sentiment data
  fetch('http://localhost:8000/api/v1/sentiment')
    .then(response => response.json())
    .then(data => {
      sentimentScore = data.sentiment_score;
      sentimentMagnitude = data.sentiment_magnitude;
    })
    .catch((error) => {
      console.error('Error:', error);
    });

  // Clear the canvas
  background(0);

  // Map the sentiment score and magnitude to color and size
  let color = map(sentimentScore, -1, 1, 0, 255);
  let movementrange = map(sentimentMagnitude, 0, 10, 0, 65);

  // if any is NaN, set to 0
  if (isNaN(color)) {
    color = 125;
  }
  if (isNaN(movementrange)) {
    movementrange = 10;
  }

  // Update and draw each ellipse
  for (let e of ellipses) {
    fill(color, 100, 100);
    noStroke();
    let movedis = random(0, movementrange);
    let moveangle = random(0, 360);
    let varx = movedis * cos(moveangle);
    let vary = movedis * sin(moveangle);
    e.locx = e.locx + varx;
    e.locy = e.locy + vary;

    // Keep the ellipse within the canvas
    e.locx = constrain(e.locx, 0, windowWidth);
    e.locy = constrain(e.locy, 0, windowHeight);

    // Draw the ellipse
    ellipse(e.locx, e.locy, e.size, e.size);
  }
}
 */

let fireParticles = [];
let sentimentScore = 0; //default score
let sentimentMagnitude = 0; //default magnitude
let bg;

function setup() {
  createCanvas(windowWidth, windowHeight);
  background(0);
  frameRate(30);

  //initialize  particles
  for (let i = 0; i < 150; i++) {
    fireParticles.push(createParticle());
  }

  bg = loadImage('background.png');
}

function draw() {
  //fetch the latest sentiment data
  fetchSentimentData();

  //clear canvas
  background(bg);

  //update and draw each fire particle
  for (let particle of fireParticles) {
    updateParticle(particle);
    drawParticle(particle);
  }
}

function fetchSentimentData() {
  fetch('http://localhost:8000/api/v1/sentiment')
    .then(response => response.json())
    .then(data => {
      sentimentScore = data.sentiment_score;
      sentimentMagnitude = data.sentiment_magnitude;
    })
    .catch(error => console.error('Error:', error));
}

function createParticle() {
  let direction = random(-1, 1);
  let speed = random(0.01, 0.07);
  let radius = random(20, 200)
  return {
    x: width * 0.68,
    y: height * 0.51,
    angle: random(0, TWO_PI),
    radius: radius,
    speed: direction * speed,
    color: color(random(200, 255), random(50), 0, 150),
  };
}

function updateParticle(particle) {
  //adjust speed based on sentiment magnitude
  speed = particle.speed + sentimentMagnitude * 0.001;

  //update angle
  particle.angle += speed;

  //adjust color based on sentiment score
  particle.color = lerpColor(color(255, 0, 0), color(0, 255, 0), (sentimentScore + 1) / 2);
}

function drawParticle(particle) {
  let x = particle.x + cos(particle.angle) * particle.radius;
  let y = particle.y + sin(particle.angle) * particle.radius;

  noStroke();
  fill(particle.color);
  ellipse(x, y, 10, 10);
}