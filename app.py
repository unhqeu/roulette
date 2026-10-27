
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="룰렛",
    page_icon="🎯",
    layout="centered"
)

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

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
    background: #FFFFFF;
    font-family: Arial, "Malgun Gothic", sans-serif;
    color: #202938;
    padding: 24px 0;
}

h1 {
    margin: 0 0 28px;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1.2px;
    text-align: center;
    color: #202938;
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
    filter: drop-shadow(0 5px 12px #1F29371A);
}

.pointer {
    position: absolute;
    z-index: 2;
    top: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 16px solid transparent;
    border-right: 16px solid transparent;
    border-top: 34px solid #26364A;
    filter: drop-shadow(0 2px 2px #00000012);
}

button {
    margin-top: 28px;
    padding: 15px 52px;
    border: none;
    border-radius: 10px;
    background: #26364A;
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s, transform 0.2s;
}

button:hover {
    background: #3B526D;
}

button:active {
    transform: translateY(1px);
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

#result {
    margin-top: 25px;
    min-height: 42px;
    font-size: 26px;
    font-weight: 800;
    text-align: center;
    color: #26364A;
    letter-spacing: -0.5px;
}
</style>
</head>

<body>

<h1>행운의 룰렛</h1>

<div class="wheel-container">
    <div class="pointer"></div>
    <canvas id="wheel" width="700" height="700"></canvas>
</div>

<button id="spinButton" onclick="spin()">룰렛 돌리기</button>
<div id="result">행운을 시험해 보세요!</div>

<script>
const TOTAL_SLICES = 50;
const sliceAngle = Math.PI * 2 / TOTAL_SLICES;

const colors = {
    "꽝": "#D9DEE5",
    "3배": "#26364A",
    "2배": "#52749B",
    "1배": "#8DA8C4",
    "1/2배": "#B8C6D5"
};

// 총 50칸: 꽝 35, 3배 1, 2배 5, 1배 5, 1/2배 4
const slices = Array(TOTAL_SLICES).fill("꽝");

// 당첨 칸을 룰렛 전체에 분산 배치
slices[0] = "3배";

[5, 15, 25, 35, 45].forEach(index => {
    slices[index] = "2배";
});

[2, 12, 22, 32, 42].forEach(index => {
    slices[index] = "1배";
});

[8, 20, 30, 40].forEach(index => {
    slices[index] = "1/2배";
});

const canvas = document.getElementById("wheel");
const ctx = canvas.getContext("2d");

const center = canvas.width / 2;
const radius = center - 10;

let currentRotation = 0;
let isSpinning = false;

function drawWheel() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    ctx.translate(center, center);
    ctx.rotate(currentRotation);

    let index = 0;

    while (index < TOTAL_SLICES) {
        const currentLabel = slices[index];
        let endIndex = index + 1;

        // 연속된 꽝 칸을 하나의 구간으로 묶기
        if (currentLabel === "꽝") {
            while (
                endIndex < TOTAL_SLICES &&
                slices[endIndex] === "꽝"
            ) {
                endIndex++;
            }
        }

        const startAngle = -Math.PI / 2 + index * sliceAngle;
        const endAngle = -Math.PI / 2 + endIndex * sliceAngle;

        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.arc(0, 0, radius, startAngle, endAngle);
        ctx.closePath();

        ctx.fillStyle = colors[currentLabel];
        ctx.fill();

        // 각 구간의 바깥 경계만 흰색으로 표시
        ctx.strokeStyle = "#FFFFFF";
        ctx.lineWidth = 2;
        ctx.stroke();

        // 각 구간에 결과 표시
        const middleAngle = (startAngle + endAngle) / 2;
        const textRadius = radius * 0.68;

        const textX = Math.cos(middleAngle) * textRadius;
        const textY = Math.sin(middleAngle) * textRadius;

        ctx.save();
        ctx.translate(textX, textY);
        ctx.rotate(middleAngle + Math.PI / 2);

        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.font = "bold 19px Arial, Malgun Gothic, sans-serif";

        if (currentLabel === "3배") {
            ctx.fillStyle = "#FFFFFF";
        } else {
            ctx.fillStyle = "#26364A";
        }

        ctx.fillText(currentLabel, 0, 0);
        ctx.restore();

        index = endIndex;
    }

    // 중앙 원
    ctx.beginPath();
    ctx.arc(0, 0, 38, 0, Math.PI * 2);
    ctx.fillStyle = "#FFFFFF";
    ctx.fill();
    ctx.strokeStyle = "#26364A";
    ctx.lineWidth = 3;
    ctx.stroke();

    // 중앙 점
    ctx.beginPath();
    ctx.arc(0, 0, 11, 0, Math.PI * 2);
    ctx.fillStyle = "#26364A";
    ctx.fill();

    ctx.restore();
}

function spin() {
    if (isSpinning) return;

    isSpinning = true;

    const button = document.getElementById("spinButton");
    const result = document.getElementById("result");

    button.disabled = true;
    result.textContent = "룰렛이 돌아가는 중...";

    // 실제 당첨 칸을 무작위로 선택
    const winnerIndex = Math.floor(Math.random() * TOTAL_SLICES);
    const winner = slices[winnerIndex];

    // 선택한 칸의 중앙이 위쪽 화살표를 향하도록 회전
    const targetAngle =
        -winnerIndex * sliceAngle - sliceAngle / 2;

    const fullRotations = 6 * Math.PI * 2;
    const normalizedCurrent =
        ((currentRotation % (Math.PI * 2)) + Math.PI * 2)
        % (Math.PI * 2);

    const normalizedTarget =
        ((targetAngle % (Math.PI * 2)) + Math.PI * 2)
        % (Math.PI * 2);

    const extraRotation =
        (normalizedTarget - normalizedCurrent + Math.PI * 2)
        % (Math.PI * 2);

    const startRotation = currentRotation;
    const finalRotation =
        startRotation + fullRotations + extraRotation;

    const duration = 5000;
    const startTime = performance.now();

    function animate(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // 처음에는 빠르게, 끝에는 천천히 감속
        const easedProgress =
            1 - Math.pow(1 - progress, 4);

        currentRotation =
            startRotation +
            (finalRotation - startRotation) * easedProgress;

        drawWheel();

        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            currentRotation = finalRotation;
            drawWheel();

            result.textContent = "결과: " + winner;

            isSpinning = false;
            button.disabled = false;
        }
    }

    requestAnimationFrame(animate);
}

drawWheel();
</script>

</body>
</html>
"""

components.html(html_code, height=780, scrolling=False)
