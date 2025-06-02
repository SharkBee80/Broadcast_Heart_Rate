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


// 设备
function refresh_devices() {
    pywebview.api.refresh_devices();
}

function update_devices(devices) {
    let device_list = document.getElementById('device-list');
    device_list.innerHTML = '';
    devices.forEach(device => {
        let li = document.createElement('li');
        li.innerText = `${device.name} - ${device.address}`;
        li.addEventListener('click', function () {
            let choiceli = document.querySelectorAll('#device-list li');
            choiceli.forEach(item => {
                item.style.backgroundColor = '';
            });
            li.style.backgroundColor = 'lightblue';
            pywebview.api.set_device(device);
        });
        device_list.appendChild(li);
    });
}

function connect_device() {
    pywebview.api.connect_device();
}

function disconnect_device() {
    pywebview.api.disconnect_device();
}

// 心率
function startFetching() {
    pywebview.api.fetch_heart_rate();
}

function stopFetching() {
    pywebview.api.stop_fetching();
}

function updateHeartRate(rate) {
    document.getElementById('heart-rate').innerText = rate;
}