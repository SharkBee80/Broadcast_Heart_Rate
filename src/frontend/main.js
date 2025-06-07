// 选项卡
let choice1 = document.querySelector('#choice-2');
choice1.style.display = 'flex';

const choice = document.querySelector('.choice');
let choiceLis = choice.querySelectorAll('li');
choiceLis.forEach(function (li) {
    li.addEventListener('click', function () {
        if (choice1) {
            choice1.style.display = 'none';
        }
        let aHref = this.querySelector('a').getAttribute('class');
        let contID = aHref.slice(0);
        let contDIv = document.getElementById(contID);
        choice1 = contDIv;
        contDIv.style.display = 'flex';
    })
})

let choiceAs = document.querySelectorAll('.choice a');
console.log(choiceAs);
choiceAs.forEach(function (a, index) {
    a.addEventListener('click', function () {
        choiceAs.forEach(function (link) {
            link.style.fontSize = '';
            link.style.backgroundColor = '#eee';
            link.style.padding = '0';
        });
        this.style.fontSize = '35px';
        this.style.backgroundColor = 'gainsboro';
        this.style.padding = '0 calc(100% / 4) 0 0';
    });
    // 判断是否是第一个 <a> 标签
    if (index === 1) {
        a.style.fontSize = '35px';
        a.style.backgroundColor = 'gainsboro';
        a.style.padding = '0 calc(100% / 4) 0 0';
    }
});

/* 初始 */
onload = function () {
    let device_data = [
        { 'name': 'iQOO WATCH 047', 'address': '88:54:8E:D9:50:47' },
        { 'name': 'EXAMPLE BLE', 'address': '12:34:56:78:90:AB' },
        { 'name': 'AAAAABBBBBCCCCCDDDDDEEEEEFFFFFGGGGG', 'address': 'XX:XX:XX:XX:XX:XX' },
        { 'name': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'address': 'AA:AA:AA:AA:AA:AA' },
    ]
    update_devices(device_data);

    chart_init();
};


// 设备
let selete_device;

function refresh_devices() {
    selete_device = null;
    pywebview.api.refresh_devices();
}

function update_devices(devices) {
    let device_list = document.getElementById('device-list');
    device_list.innerHTML = '';
    if (devices.length === 0) {
        let li = document.createElement('li');
        li.innerText = 'No devices found';
        device_list.appendChild(li);
        return;
    }
    devices.forEach(device => {
        let li = document.createElement('li');
        li.innerText = `${device.name} - ${device.address}`;
        li.addEventListener('click', function () {
            let choiceli = document.querySelectorAll('#device-list li');
            choiceli.forEach(item => {
                item.style.backgroundColor = '';
            });
            li.style.backgroundColor = 'lightskyblue';
            set_device(device);
        });
        device_list.appendChild(li);
    });
}

function set_device(device) {
    pywebview.api.set_device(device);
    selete_device = device;
}

function connect_device() {
    if (!selete_device) {
        alert('Please select a device first.');
        return;
    }
    pywebview.api.connect_device();
}

/* 列表状态 */
function ListState(state) {
    let list = document.getElementById('device-list');

    switch (state) {
        case true:
            list.classList.remove('disabled');
            break;
        case false:
            list.classList.add('disabled');
            break;
    }
}

function disconnect_device() {
    pywebview.api.disconnect_device();
}

/* 按钮状态 */
function ButtonState(id, state, text) {
    let btn = document.getElementById(id);
    switch (state) {
        case true:
            btn.disabled = false;
            btn.innerText = text;
            break;
        case false:
            btn.disabled = true;
            btn.innerText = text;
            break;
    }
}

// 心率
let heart_rate_status = false;
let heart_rate;
let heart_rate_time = 0;
let heart_rate_interval;

function startHeartRate(state) {
    heart_rate_status = state;
    if (heart_rate_status) {
        heart_rate_interval = setInterval(calc_heart_rate, 1000); // 每秒更新一次
    } else if (heart_rate_interval) {
        clearInterval(heart_rate_interval);
    }
}

function getHeartRate(rate) {
    heart_rate = rate;
    heart_rate_time = Date.now();
}

function calc_heart_rate() {
    if (Date.now() - heart_rate_time > 2000) {
        heart_rate = null;
    }
    updateChart(heart_rate);
}