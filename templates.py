######################################################
#Desarrollado por: Jeremías Emmanuel Miranda         #
#Template para mostrar la información en el WebServer#
######################################################

HTML = """<!DOCTYPE html>
<html>
<head>
<title>Gas Monitor</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>
<body>

<h2>Monitor de Gases</h2>

<canvas id="chart" width="400" height="200"></canvas>

<p id="temp"></p>
<p id="hum"></p>
<p id="estado"></p>

<script>
const MAX_PUNTOS = 20; //Cantidad de puntos a últimos mantener
const UMBRAL_ALERTA = 3; //Umbral de alertas

let labels = [];
let mq2 = [];
let mq3 = [];
let mq135 = [];

const ctx = document.getElementById('chart').getContext('2d');

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [
            { 
                label: 'MQ2', 
                data: mq2,
                borderColor: 'blue'
            },
            { 
                label: 'MQ3', 
                data: mq3,
                borderColor: 'green'
            },
            { 
                label: 'MQ135', 
                data: mq135,
                borderColor: 'orange'
            },
            {
                label: 'Umbral',
                data: Array(MAX_PUNTOS).fill(UMBRAL_ALERTA),
                borderColor: 'red',
                borderDash: [5, 5],
                fill: false
            }
        ]
    },
    options: {
        animation: false,
        scales: {
            y: { beginAtZero: true }
        }
    }
});

async function update() {
    let res = await fetch('/data');
    let d = await res.json();

    let now = new Date().toLocaleTimeString();

    labels.push(now);
    mq2.push(d.mq2);
    mq3.push(d.mq3);
    mq135.push(d.mq135);

    // mantener últimos puntos
    if (labels.length > MAX_PUNTOS) {
        labels.shift();
        mq2.shift();
        mq3.shift();
        mq135.shift();
    }

    chart.update();
    
    document.getElementById("temp").innerText = "Temperatura: " + d.temp + " C";
    document.getElementById("hum").innerText = "Humedad: " + d.hum + "%";

    document.getElementById("estado").innerText = "Estado: " + d.estado;
    
    document.body.style.backgroundColor =
        d.estado === "ALERTA" ? "#ff4d4d" :
        d.estado === "WARN" ? "#fff176" :
        "#ffffff";
}

setInterval(update, 2000);
update();
</script>

</body>
</html>
"""