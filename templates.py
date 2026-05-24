######################################################
#Desarrollado por: Jeremías Emmanuel Miranda         #
#Template para mostrar la información en el WebServer#
######################################################

HTML = """<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">
<title>Gas Monitor</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
    font-family: Arial;
    margin:20px;
    background:#f2f2f2;
    transition:0.3s;
}

h2{
    text-align:center;
}

.card{
    background:white;
    padding:15px;
    border-radius:10px;
    margin-bottom:15px;
    box-shadow:0 0 10px rgba(0,0,0,0.1);
}

.estado{
    font-size:24px;
    font-weight:bold;
    text-align:center;
    padding:10px;
    border-radius:10px;
}

.normal{
    background:#c8e6c9;
    color:#1b5e20;
}

.alerta{
    background:#ffccbc;
    color:#b71c1c;
}

.multi{
    background:#ff5252;
    color:white;
}

.grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:10px;
}

.sensor{
    background:#fafafa;
    padding:10px;
    border-radius:8px;
    text-align:center;
}

.valor{
    font-size:22px;
    font-weight:bold;
}

small{
    color:#666;
}

</style>

</head>

<body>

<h2>Monitor Inteligente de Gases</h2>

<div id="estadoBox" class="estado normal">
    INICIANDO...
</div>

<br>

<div class="grid">

    <div class="sensor">
        <h3>MQ2</h3>
        <div class="valor" id="ppm2">0</div>
        <small>ppm combustible</small>
    </div>

    <div class="sensor">
        <h3>MQ3</h3>
        <div class="valor" id="ppm3">0</div>
        <small>alcohol/gases</small>
    </div>

    <div class="sensor">
        <h3>MQ135</h3>
        <div class="valor" id="ppm135">0</div>
        <small>calidad aire</small>
    </div>

    <div class="sensor">
        <h3>Clima</h3>
        <div id="temp">0 C</div>
        <div id="hum">0 %</div>
    </div>

</div>

<br>

<div class="card">
    <canvas id="chart"></canvas>
</div>

<script>

const MAX_PUNTOS = 20;

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
                borderColor: 'blue',
                tension:0.2
            },

            {
                label: 'MQ3',
                data: mq3,
                borderColor: 'green',
                tension:0.2
            },

            {
                label: 'MQ135',
                data: mq135,
                borderColor: 'orange',
                tension:0.2
            }
        ]
    },

    options: {

        animation:false,

        responsive:true,

        scales:{
            y:{
                beginAtZero:true
            }
        }
    }
});

async function update(){

    try{

        let res = await fetch('/data');

        let d = await res.json();

        let now = new Date().toLocaleTimeString();

        // =========================
        // GRAFICO
        // =========================

        labels.push(now);

        mq2.push(d.ppm2);
        mq3.push(d.ppm3);
        mq135.push(d.ppm135);

        if(labels.length > MAX_PUNTOS){

            labels.shift();

            mq2.shift();
            mq3.shift();
            mq135.shift();
        }

        chart.update();

        // =========================
        // DATOS
        // =========================

        document.getElementById("ppm2").innerText = d.ppm2 + " ppm";
        document.getElementById("ppm3").innerText = d.ppm3 + " ppm";
        document.getElementById("ppm135").innerText = d.ppm135 + " ppm";

        document.getElementById("temp").innerText =
            d.temp + " C";

        document.getElementById("hum").innerText =
            d.hum + " %";

        // =========================
        // ESTADO
        // =========================

        const estadoBox = document.getElementById("estadoBox");

        estadoBox.innerText = d.estado;

        estadoBox.className = "estado";

        if(d.estado === "NORMAL"){

            estadoBox.classList.add("normal");
            document.body.style.background = "#f2f2f2";
        }

        else if(d.estado === "MULTIGAS"){

            estadoBox.classList.add("multi");
            document.body.style.background = "#ffebee";
        }

        else{

            estadoBox.classList.add("alerta");
            document.body.style.background = "#fff3e0";
        }

    }catch(err){

        console.log(err);
    }
}

setInterval(update, 2000);

update();

</script>

</body>
</html>
"""