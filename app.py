
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>행운의 룰렛</title>
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #f3f4f8;
    font-family: Arial, "Malgun Gothic", sans-serif;
    color: #222;
}

h1 {
    margin: 0 0 24px;
    font-size: 32px;
}

.wheel-container {
    position: relative;
    width: min(88vw, 460px);
    aspect-ratio: 1;
}

canvas {
    width: 100%;
    height: 100%;
    display: block;
    filter: drop-shadow(0 7px 10px #0002);
}

.pointer {
    position: absolute;
    z-index: 2;
    top: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 19px solid transparent;
    border-right: 19px solid transparent;
    border-top: 38px solid #222;
}

button {
    margin-top: 28px;
    padding: 15px 55px;
    border: none;
    border-radius: 14px;
    background: #6255e7;
    color: white;
    font-size: 21px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 5px 0 #4539b6;
}

button:hover { background: #5145d3; }
button:disabled { opacity: 0.6; cursor: not-allowed; }

#result {
    margin-top: 24px;
    min-height: 42px;
    font-size: 27px;
    font-weight: bold;
    text-align: center;
}
</style>
</head>
<body>

<h1>🎯 행운의 룰렛</h1>

<div class="wheel-container">
    <div class="pointer"></div>
    <canvas id="wheel" width="700" height="700"></canvas>
</div>

<button id="spinButton" onclick="spin()">룰렛 돌리기!</button>
<div id="result">과연 결과는?</div>

<script>
const canvas = document.getElementById("wheel");
const ctx = canvas.getContext("2d");
const button = document.getElementById("spinButton");
const result = document.getElementById("result");

// 꽝 70%, 나머지 확률은 기존 비율 유지
const outcomes = [
    { label: "-10", weight: 8.1, color: "#5b8def" },
    { label: "꽝", weight: 14, color: "#aeb4c0" },
    { label: "0배", weight: 3.6, color: "#52c7a5" },
    { label: "꽝", weight: 14, color: "#aeb4c0" },
    { label: "3배", weight: 4.5, color: "#ffca58" },
    { label: "꽝", weight: 14, color: "#aeb4c0" },
    { label: "+10", weight: 8.1, color: "#f07878" },
    { label: "꽝", weight: 14, color: "#aeb4c0" },
    { label: "2배", weight: 5.7, color: "#b18bea" },
    { label: "꽝", weight: 14, color: "#aeb4c0" }
];

const totalWeight = outcomes.reduce((sum, item) => sum + item.weight, 0);

let rotation = 0;
let spinning = false;

function drawWheel() {
    const center = 350;
    const radius = 330;

    ctx.clearRect(0, 0, 700, 700);
    ctx.save();
    ctx.translate(center, center);
    ctx.rotate(rotation);

    let startAngle = -Math.PI / 2;

    outcomes.forEach(item => {
        const sliceAngle = item.weight / totalWeight * Math.PI * 2;
        const endAngle = startAngle + sliceAngle;
        const middleAngle = startAngle + sliceAngle / 2;

        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.arc(0, 0, radius, startAngle, endAngle);
        ctx.closePath();
        ctx.fillStyle = item.color;
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 4;
        ctx.stroke();

        ctx.save();
        ctx.rotate(middleAngle);
        ctx.translate(radius * 0.66, 0);
        ctx.rotate(Math.PI / 2);
        ctx.fillStyle = "#222";
        ctx.font = "bold 29px Arial, sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(item.label, 0, 0);
        ctx.restore();

        startAngle = endAngle;
    });

    ctx.beginPath();
    ctx.arc(0, 0, 43, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    ctx.strokeStyle = "#333333";
    ctx.lineWidth = 5;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(0, 0, 13, 0, Math.PI * 2);
    ctx.fillStyle = "#6255e7";
    ctx.fill();

    ctx.restore();
}

function chooseWinner() {
    let random = Math.random() * totalWeight;

    for (const item of outcomes) {
        random -= item.weight;
        if (random < 0) return item;
    }

    return outcomes[outcomes.length - 1];
}

function spin() {
    if (spinning) return;

    spinning = true;
    button.disabled = true;
    result.textContent = "돌아가는 중...";

    const winner = chooseWinner();
    const winnerIndex = outcomes.indexOf(winner);

    let accumulated = 0;
    for (let i = 0; i < winnerIndex; i++) {
        accumulated += outcomes[i].weight / totalWeight * Math.PI * 2;
    }

    const sliceAngle = winner.weight / totalWeight * Math.PI * 2;
    const middleAngle = accumulated + sliceAngle / 2;

    const fullTurns = 6 + Math.floor(Math.random() * 3);
    const currentNormalized =
        ((rotation % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
    const desiredNormalized =
        ((-middleAngle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
    const extraAngle =
        (desiredNormalized - currentNormalized + Math.PI * 2) % (Math.PI * 2);

    const startRotation = rotation;
    const endRotation = rotation + fullTurns * Math.PI * 2 + extraAngle;
    const duration = 5000;
    const startTime = performance.now();

    function animate(now) {
        const progress = Math.min((now - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 4);

        rotation = startRotation + (endRotation - startRotation) * eased;
        drawWheel();

        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            rotation = endRotation;
            drawWheel();
            result.textContent = "결과: " + winner.label;
            spinning = false;
            button.disabled = false;
        }
    }

    requestAnimationFrame(animate);
}

drawWheel();
</script>

</body>
</html>
