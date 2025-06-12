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
        //{ 'name': 'EXAMPLE BLE', 'address': '12:34:56:78:90:AB' },
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

let eventSource;
let eventSourceTimeout;
/*
function startHeartRate(state) {
    if (typeof state !== 'boolean') {
        console.warn('Invalid state type, expected boolean');
        return;
    }
    heart_rate_status = state;
    if (heart_rate_interval) {
        clearInterval(heart_rate_interval);
        heart_rate_interval = null;
    }
    if (heart_rate_status) {
        heart_rate_interval = setInterval(fetch_heart_rate, 1000); // 每秒更新一次
    }
}
*/

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
    } else {
        if (eventSource) {
            clearTimeout(eventSourceTimeout);
            eventSourceTimeout = setTimeout(() => {
                if (eventSource) {
                    eventSource.close();
                    eventSource = null;
                }
            }, 3000);
        }
    }
}

function getHeartRate(rate) {
    heart_rate = rate;
    heart_rate_time = Date.now();
}

//api

async function fetch_heart_rate() {
    let timeoutId;
    try {
        const controller = new AbortController();
        timeoutId = setTimeout(() => controller.abort(), 500);

        const response = await fetch('/api', {
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        //{'rate':72}
        const rate = JSON.parse(data).rate;
        updateChart(rate);
    } catch (error) {
        console.error('Failed to fetch rate data:', error);
    }
}

//sse
function listen_heart_rate() {
    eventSource = new EventSource('/sse1');

    eventSource.onmessage = function (event) {
        const data = JSON.parse(event.data);
        //"{\"rate\": 71, \"time\": \"22:45:32\"}"
        const rate = data.rate
        updateChart(rate);
    };
    eventSource.onerror = function (error) {
        console.error('Failed to receive rate data:', error);
    }
}

// 网页
function set_html_files(files) {
    createCards(files);
}

function createCards(items) {
    const container = document.getElementById('card-container');
    container.innerHTML = '';

    // 为每个项目创建卡片
    items.forEach(item => {
        const host = window.location.origin; //  获取当前页面的域名
        const url = host + '/web/' + item.html;
        const image = host + '/web/' + item.image;

        // 创建卡片元素
        const card = document.createElement('div');
        card.className = 'square-card';

        // 图片部分
        const imageDiv = document.createElement('div');
        imageDiv.className = 'image-container';

        const img = document.createElement('img');
        img.src = image;
        img.alt = item.name;
        imageDiv.appendChild(img);

        imageDiv.addEventListener('click', function () {
            const cards = container.querySelectorAll('.square-card')
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
    if (items.length % 5 !== 0) {
        for (let i = 0; i < 5 - items.length % 5; i++) {
            let card = document.createElement('div');
            card.classList.add('square-card');
            //card.style.boxShadow = '0 0 0 rgba(0, 0, 0, 0)';
            container.appendChild(card);
        }
    }
}

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
        { 'section': 'server', 'option': 'host', 'value': document.getElementById('server_host').value },
        { 'section': 'server', 'option': 'port', 'value': document.getElementById('server_port').value },
        { 'section': 'float', 'option': 'open', 'value': document.getElementById('float_open').checked },
    ]
    pywebview.api.save_setting(settings);
    alert('保存成功\n请重新启动软件');
}