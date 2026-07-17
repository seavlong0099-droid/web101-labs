let scores = [];

displayScores();

function displayScores(){

    let html = "";

    for(let score of scores){

        let color = "orange";

        if(score >= 80)
            color = "green";
        else if(score < 50)
            color = "red";

        html += `<div class="score ${color}">${score}</div>`;
    }

    document.getElementById("scores").innerHTML = html;

    let highest = Math.max(...scores);
    let lowest = Math.min(...scores);

    let total = 0;

    for(let s of scores){
        total += s;
    }

    let average = (total / scores.length).toFixed(1);

    document.getElementById("summary").innerHTML =
    `Highest: ${highest} | Lowest: ${lowest} | Average: ${average}`;
}

function addScore(){

    let input = document.getElementById("newScore");
    let score = Number(input.value);

    if(score < 0 || score > 100 || input.value==""){
        alert("Enter a score between 0 and 100");
        return;
    }

    scores.push(score);

    input.value="";

    displayScores();
}