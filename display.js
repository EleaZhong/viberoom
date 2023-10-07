// p5.js script for visualizing sentiment data

let sentimentScore;
let sentimentMagnitude;

let ellipses = [];

function setup() {
  createCanvas(windowWidth, windowHeight);
  background(0);
  frameRate(10); // Limit the frame rate to prevent excessive querying

  // Create multiple ellipses
  for (let i = 0; i < 10; i++) {
    ellipses.push({
      locx: random(windowWidth),
      locy: random(windowHeight),
      size: random(10, 100)
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
  let movementrange = map(sentimentMagnitude, 0, 10, 0, 40);

  // if any is NaN, set to 0
  if (isNaN(color)) {
    color = 0;
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