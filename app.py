
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

const TOTAL_SLICES = 50;
const sliceAngle = Math.PI * 2 / TOTAL_SLICES;

const colors = {
    "꽝": "#aeb4c0",
    "3배": "#ffca58",
    "2배": "#b18bea",
    "1배": "#52c7a5",
    "1/2배": "#f07878"
};


const slices = new Array(50).fill(null);

// 3배: 한 칸
slices[0] = { label: "3배", color: colors["3배"] };

// 2배: 3배와 멀리 떨어진 위치에 배치
[10, 20, 30, 40].forEach(index => {
    slices[index] = { label: "2배", color: colors["2배"] };
});

// 나머지 비꽝 결과를 전체에 분산
const otherResults = [
    { label: "2배", color: colors["2배"] },
    { label: "1배", color: colors["1배"] },
    { label: "1배", color: colors["1배"] },
    { label: "1배", color: colors["1배"] },
    { label: "1배", color: colors["1배"] },
    { label: "1배", color: colors["1배"] },
    { label: "1/2배", color: colors["1/2배"] },
    { label: "1/2배", color: colors["1/2배"] },
    { label: "1/2배", color: colors["1/2배"] },
    { label: "1/2배", color: colors["1/2배"] }
];

// 각 구간에 비꽝 결과를 하나씩 배치
const positions = [5, 15, 25, 35, 45, 7, 17, 27, 37, 47];

positions.forEach((index, i) => {
    slices[index] = otherResults[i];
});

// 남은 칸은 모두 꽝
for (let i = 0; i < 50; i++) {
    if (slices[i] === null) {
        slices[i] = {
            label: "꽝",
            color: colors["꽝"]
        };
    }
}

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

    let index = 0;

    while (index < TOTAL_SLICES) {
        const item = slices[index];
        let endIndex = index + 1;

        // 연속된 꽝 칸을 하나의 구역으로 합치기
        if (item.label === "꽝") {
            while (
                endIndex < TOTAL_SLICES &&
                slices[endIndex].label === "꽝"
            ) {
                endIndex++;
            }
        }

        const startAngle =
            -Math.PI / 2 + index * sliceAngle;

        const endAngle =
            -Math.PI / 2 + endIndex * sliceAngle;

        const middleAngle =
            (startAngle + endAngle) / 2;

        // 구역 그리기
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.arc(
            0, 0, radius,
            startAngle, endAngle
        );
        ctx.closePath();

        ctx.fillStyle = item.color;
        ctx.fill();

        // 구역의 바깥 경계만 표시
        // 이웃한 꽝 사이에는 경계선이 생기지 않음
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.stroke();

        // 결과 글자 표시
        ctx.save();
        ctx.rotate(middleAngle);
        ctx.translate(radius * 0.76, 0);
        ctx.rotate(Math.PI / 2);

        ctx.fillStyle = "#222";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        if (item.label === "꽝") {
            ctx.font = "bold 17px Arial, sans-serif";
        } else {
            ctx.font = "bold 13px Arial, sans-serif";
        }

        ctx.fillText(item.label, 0, 0);

        ctx.restore();

        index = endIndex;
    }

    // 중앙 장식
    ctx.beginPath();
    ctx.arc(0, 0, 38, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();

    ctx.strokeStyle = "#333333";
    ctx.lineWidth = 4;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(0, 0, 12, 0, Math.PI * 2);
    ctx.fillStyle = "#6255e7";
    ctx.fill();

    ctx.restore();
}

// 당첨될 확률 단위 선택
function chooseWinner() {
    return Math.floor(Math.random() * TOTAL_SLICES);
}

// 룰렛 회전
function spin() {
    if (spinning) return;

    spinning = true;
    button.disabled = true;
    result.textContent = "돌아가는 중...";

    // 50개 단위 중 하나를 선택
    const winnerIndex = chooseWinner();
    const winner = slices[winnerIndex];

    // 선택한 단위의 중앙을 포인터에 맞춤
    const middleAngle =
        winnerIndex * sliceAngle + sliceAngle / 2;

    const fullTurns =
        6 + Math.floor(Math.random() * 3);

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
        rotation +
        fullTurns * Math.PI * 2 +
        extraAngle;

    const duration = 5000;
    const startTime = performance.now();

    function animate(now) {
        const progress = Math.min(
            (now - startTime) / duration,
            1
        );

        // 부드럽게 감속
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
