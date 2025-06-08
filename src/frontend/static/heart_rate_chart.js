// 获取DOM元素
const ctx = document.getElementById('heartRateChart').getContext('2d');

const currentRateSpan = document.getElementById('heart-rate');

// 初始化数据
let heartRateData = [];
let labels = [];
const maxDataPoints = 32; // 图表上显示的最大数据点数

let updateInterval;
let isSimulating = false;

// 创建图表
const heartRateChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: '心率 (BPM)',
            data: heartRateData,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.1)',
            borderWidth: 2,
            tension: 0.5,  // 增加这个值使曲线更平滑 (0-1之间)
            fill: true,
            cubicInterpolationMode: 'monotone'  // 使用单调插值模式
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: false,
                suggestedMin: 40,
                suggestedMax: 120,
                title: {
                    display: true,
                    text: '心率 (BPM)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: '时间'
                }
            }
        },
        animation: {
            duration: 0 // 禁用动画以获得更流畅的更新
        }
    }
});

/*
// 生成模拟心率数据 (60-100之间的随机值，偶尔会有波动)
function generateHeartRate() {
    // 基础心率在60-80之间
    let baseRate = 60 + Math.random() * 20;

    // 偶尔会有较大的波动
    if (Math.random() < 0.1) {
        baseRate += (Math.random() - 0.5) * 30;
    }

    // 确保心率在合理范围内
    return Math.max(40, Math.min(120, Math.round(baseRate)));
}
*/
// 更新图表数据
function updateChart(rate) {
    //const newRate = generateHeartRate();
    const newRate = rate;

    // 添加新数据
    heartRateData.push(newRate ? newRate : 0);
    labels.push(new Date().toLocaleTimeString());

    // 如果数据点超过最大值，移除最旧的数据
    if (heartRateData.length > maxDataPoints) {
        heartRateData.shift();
        labels.shift();
    }

    // 更新当前心率显示
    currentRateSpan.textContent = newRate ? newRate : '--';

    // 更新图表
    heartRateChart.update();
}


function chart_init() {
    // 初始化空数据
    for (let i = 0; i < maxDataPoints; i++) {
        heartRateData.push(null);
        labels.push('              ');  //[              ]14=6*2+2
    }
    heartRateChart.update();
}

/*
// 初始化
window.addEventListener('load', () => {
    chart_init();

    if (!isSimulating) {
        isSimulating = true;
        updateInterval = setInterval(updateChart, 1000); // 每秒更新一次
    }
});
*/