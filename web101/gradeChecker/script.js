function checkGrade(){

    let score = Number(document.getElementById("score").value);

    let grade = "";

    if(score < 0 || score > 100){
        document.getElementById("result").innerHTML = "Please enter a valid score!";
        return;
    }

    if(score >= 90){
        grade = "A";
    }
    else if(score >= 80){
        grade = "B";
    }
    else if(score >= 70){
        grade = "C";
    }
    else if(score >= 60){
        grade = "D";
    }
    else{
        grade = "F";
    }

    document.getElementById("result").innerHTML =
    `Score: ${score} - Grade ${grade}`;
}