// 选项卡
let choice1 = document.querySelector('#choice-2');
choice1.style.display = 'flex';

const choice = document.querySelector('.choice');
let choiceLis = choice.querySelectorAll('li');
choiceLis.forEach(function (li) {
    li.addEventListener('click', function () {
        if (choice1) {
            choice1.style.display = '';
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
            link.style.backgroundColor = '';
            link.style.padding = '';
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
        { 'name': '点击刷新以开始', 'address': '>>>>' },
        //{ 'name': 'iQOO WATCH 047', 'address': '88:54:8E:D9:50:47' },
        //{ 'name': 'AAAAABBBBBCCCCCDDDDDEEEEEFFFFFGGGGG', 'address': 'XX:XX:XX:XX:XX:XX' },
        //{ 'name': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'address': 'AA:AA:AA:AA:AA:AA' },
    ]
    update_devices(device_data);

    chart_init();

    this.setTimeout(() => pywebview.api.onload_init(), 100);
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
        let device_rssi;
        if (!device.rssi) device_rssi = ''; else device_rssi = `[${device.rssi}]`;
        li.innerText = `${device.name} - ${device.address} ${device_rssi}`;
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

function validateMAC(address) {
    const macRegex = /^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$/;
    return macRegex.test(address);
}

function set_device(device) {
    if (!validateMAC(device.address)) {
        return;
    }
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

let eventSource;
let eventSourceTimeout;


function startHeartRate(state) {
    if (typeof state !== 'boolean') {
        console.warn('Invalid state type, expected boolean');
        return;
    }
    heart_rate_status = state;
    // 清除已有定时器
    if (eventSourceTimeout) {
        clearTimeout(eventSourceTimeout);
        eventSourceTimeout = null;
    }

    if (heart_rate_status) {
        if (!eventSource) listen_heart_rate();
        updateChartThread(true);
    } else {
        if (eventSource) {
            //clearTimeout(eventSourceTimeout);
            eventSourceTimeout = setTimeout(() => {
                if (eventSource) {
                    eventSource.close();
                    eventSource = null;
                    updateChartThread(false);
                }
            }, 3000);
        }
    }
}

let updateChartInterval;

/**
 * 
 * @param {boolean} enabled 
 */
function updateChartThread(enabled) {
    if (enabled) {
        if (updateChartInterval) clearInterval(updateChartInterval);
        updateChartInterval = setInterval(()=>{
            updateChart(heartRate);
        },1000);
    } else {
        setTimeout(()=>{
            clearInterval(updateChartInterval);
        },2000);
    }
}

let heartRate = null;
//sse
function listen_heart_rate() {
    eventSource = new EventSource('/sse1');

    eventSource.onmessage = function (event) {
        const data = JSON.parse(event.data);
        //"{\"rate\": 71, \"time\": \"22:45:32\"}"
        heartRate = data.rate
    };
    eventSource.onerror = function (error) {
        console.error('Failed to receive rate data:', error);
        heartRate = null;
    }
    eventSource.close = function () {
        console.log('Disconnected from the server');
        heartRate = null;
    }
}

// 网页
function set_html_files(files) {
    createCards(files);
}

const container = document.getElementById('card-container');
let cards_length = 0;
function createCards(items) {
    container.innerHTML = '';

    // 为每个项目创建卡片
    cards_length = items.length
    items.forEach(item => {
        const host = window.location.origin; //  获取当前页面的域名
        const url = host + '/web/' + item.html;
        const image = host + '/web/' + item.image;

        // 创建卡片元素
        const card = document.createElement('div');
        card.className = 'card';

        // 图片部分
        const imageDiv = document.createElement('div');
        imageDiv.className = 'image-container';

        const img = document.createElement('img');
        img.src = image;
        img.alt = item.name;
        imageDiv.appendChild(img);

        imageDiv.addEventListener('click', function () {
            const cards = container.querySelectorAll('.card')
            cards.forEach(item => {
                item.style.outline = '';
            });
            card.style.outline = '1px solid darkgreen';
            set_url(url);
        });

        // 名字部分
        const nameDiv = document.createElement('div');
        nameDiv.className = 'name';
        nameDiv.textContent = item.name;

        // 按钮部分
        const buttonsDiv = document.createElement('div');
        buttonsDiv.className = 'buttons';

        const copyButton = document.createElement('div');
        copyButton.className = 'button copy';
        copyButton.textContent = '复制';
        copyButton.addEventListener('click', () => {
            navigator.clipboard.writeText(url)
                .then(() => alert("已复制: " + url))
                .catch(err => alert("复制失败：" + err));
        });

        const openButton = document.createElement('div');
        openButton.className = 'button open';
        openButton.textContent = '打开';
        openButton.addEventListener('click', () => {
            window.open(url);
        });

        buttonsDiv.appendChild(copyButton);
        buttonsDiv.appendChild(openButton);

        // 组装卡片
        card.appendChild(imageDiv);
        card.appendChild(nameDiv);
        card.appendChild(buttonsDiv);

        // 添加到容器
        container.appendChild(card);
    });

    // 填充空白
    format_card();
}

let cards_fake = 0;
function format_card() {
    const container_clientWidth = window.outerWidth * 0.82 * 0.98;
    const eachline = Math.floor(container_clientWidth / (107 + 2 + 8));
    const remainder = cards_length % eachline;

    if ((remainder === 0 ? 0 : eachline - remainder) === cards_fake) return;

    cards_fake = remainder === 0 ? 0 : eachline - remainder;

    const fake_cards = container.querySelectorAll('.fake_card');
    if (fake_cards.length > 0) {
        fake_cards.forEach(fake_card => {
            fake_card.remove();
        });
    };
    if (cards_fake == 0) return;
    for (let i = 0; i < cards_fake; i++) {
        const card = document.createElement('div');
        card.className = 'card fake_card';
        //card.style.boxShadow = '0 0 0 rgba(0, 0, 0, 0)';
        container.appendChild(card);
    };
};

// onresize
window.onresize = () => {
    format_card();
};

// 浮窗
function set_url(url) {
    pywebview.api.set_url(url);
}

const switchs = document.querySelectorAll('.switch input[type="checkbox"]');
switchs.forEach(switch_ => {
    switch_.addEventListener('click', function () {
        pywebview.api.switch_toggle(switch_.id, switch_.checked);
    });
});

// 设置
function set_switch(id, state) {
    switch_name = id;
    switch_state = state;
    const switchs = document.querySelectorAll('input[type="checkbox"]');
    switchs.forEach(switch_ => {
        if (switch_.id === id) {
            switch_.checked = state;
        }
    });
}

function set_text(id, text) {
    const text_ = document.getElementById(id);
    text_.value = text;
}

function setting_save() {
    const settings = [
        //server
        { 'section': 'server', 'option': 'host', 'value': document.getElementById('server_host').value },
        { 'section': 'server', 'option': 'port', 'value': document.getElementById('server_port').value },
        //start
        { 'section': 'start', 'option': 'refresh', 'value': document.getElementById('start_refresh').checked },
        //float
        { 'section': 'float', 'option': 'open', 'value': document.getElementById('float_open').checked },
    ]
    pywebview.api.save_setting(settings);
}

function setting_reset() {
    pywebview.api.reset_setting();
}