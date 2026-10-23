
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="룰렛",
    layout="wide"
)

html_code = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>행운의 룰렛</title>

<style>
* {
    box-sizing: border-box;
}

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
    padding: 20px 0;
}

h1 {
    margin: 0 0 24px;
    font-size: 32px;
    text-align: center;
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

button:hover {
    background: #5145d3;
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

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

// 룰렛 확률 설정: 총 50칸, 한 칸당 2%
const outcomes = [
    { label: "꽝", count: 35, color: "#aeb4c0" },
    { label: "3배", count: 1, color: "#ffca58" },
    { label: "2배", count: 5, color: "#b18bea" },
    { label: "1배", count: 5, color: "#52c7a5" },
    { label: "1/2배", count: 4, color: "#f07878" }
];

// 각 결과를 실제 룰렛의 개별 칸으로 변환
const slices = [];

outcomes.forEach(item => {
    for (let i = 0; i < item.count; i++) {
        slices.push({
            label: item.label,
            color: item.color
        });
    }
});

// 총 50칸
const totalSlices = slices.length;
const sliceAngle = Math.PI * 2 / totalSlices;

let rotation = 0;
let spinning = false;

// 룰렛 그리기
function drawWheel() {
    const center = 350;
    const radius = 330;

    ctx.clearRect(0, 0, 700, 700);

    ctx.save();
    ctx.translate(center, center);
    ctx.rotate(rotation);

    slices.forEach((item, index) => {
        const startAngle = -Math.PI / 2 + index * sliceAngle;
        const endAngle = startAngle + sliceAngle;
        const middleAngle = startAngle + sliceAngle / 2;

        // 칸 그리기
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.arc(0, 0, radius, startAngle, endAngle);
        ctx.closePath();

        ctx.fillStyle = item.color;
        ctx.fill();

        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.stroke();

        // 칸에 결과 표시
        ctx.save();
        ctx.rotate(middleAngle);
        ctx.translate(radius * 0.79, 0);
        ctx.rotate(Math.PI / 2);

        ctx.fillStyle = "#222";
        ctx.font = "bold 15px Arial, sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        ctx.fillText(item.label, 0, 0);

        ctx.restore();
    });

    // 중앙 장식
    ctx.beginPath();
    ctx.arc(0, 0, 35, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();

    ctx.strokeStyle = "#333333";
    ctx.lineWidth = 4;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(0, 0, 11, 0, Math.PI * 2);
    ctx.fillStyle = "#6255e7";
    ctx.fill();

    ctx.restore();
}

// 확률에 따라 당첨 결과 선택
function chooseWinner() {
    const randomIndex = Math.floor(Math.random() * totalSlices);
    return randomIndex;
}

// 룰렛 회전
function spin() {
    if (spinning) return;

    spinning = true;
    button.disabled = true;
    result.textContent = "돌아가는 중...";

    // 당첨될 칸 선택
    const winnerIndex = chooseWinner();
    const winner = slices[winnerIndex];

    // 선택된 칸의 중앙이 포인터를 향하도록 계산
    const middleAngle =
        winnerIndex * sliceAngle + sliceAngle / 2;

    const fullTurns = 6 + Math.floor(Math.random() * 3);

    const currentNormalized =
        ((rotation % (Math.PI * 2)) + Math.PI * 2)
        % (Math.PI * 2);

    const desiredNormalized =
        ((-middleAngle % (Math.PI * 2)) + Math.PI * 2)
        % (Math.PI * 2);

    const extraAngle =
        (desiredNormalized - currentNormalized + Math.PI * 2)
        % (Math.PI * 2);

    const startRotation = rotation;

    const endRotation =
        rotation + fullTurns * Math.PI * 2 + extraAngle;

    const duration = 5000;
    const startTime = performance.now();

    function animate(now) {
        const progress = Math.min(
            (now - startTime) / duration,
            1
        );

        const eased = 1 - Math.pow(1 - progress, 4);

        rotation =
            startRotation +
            (endRotation - startRotation) * eased;

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

// 처음 화면 표시
drawWheel();
</script>

</body>
</html>
"""

components.html(
    html_code,
    height=800,
    scrolling=False
)
