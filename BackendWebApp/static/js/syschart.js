
var cpuData = [];
var ramData = [];
var chart = new ApexCharts(document.getElementById('chart'), {
    series: [{
        name: 'CPU Percent',
        data: cpuData
    }, {
        name: 'RAM Percent',
        data: ramData
    }],
    chart: {
        type: 'line',
        height: 350,
        animations: {
            enabled: true,
            easing: 'linear',
            dynamicAnimation: {
                speed: 1000
            }
        },
    },
    xaxis: {
        type: 'datetime',
        tickAmount: 6,
    },
    yaxis: {
        min: 0,
        max: 100,
    },
    legend: {
        show: true,
        position: 'top',
    },
});
chart.render();

function updateSystemInfo() {
    fetch('sysinfo/jsondata')
        .then(response => response.json())
        .then(data => {
            document.getElementById('cpu_percent').innerText = data.cpu_percent;
            document.getElementById('ram_percent').innerText = data.ram_percent;

            var now = new Date().getTime();
            cpuData.push({ x: now, y: data.cpu_percent });
            ramData.push({ x: now, y: data.ram_percent });

            if (cpuData.length > 10) {
                cpuData.shift();
            }
            if (ramData.length > 10) {
                ramData.shift();
            }

            chart.updateSeries([{
                data: cpuData
            }, {
                data: ramData
            }]);
        });
}
setInterval(updateSystemInfo, 1000); // Update every second (1000ms)