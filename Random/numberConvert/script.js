function convertNumber(){

    let number = document.getElementById("numberInput").value;

    let words = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine"
    ];

    let result = "";

    for(let i = 0; i < number.length; i++){

        let digit = number[i];

        result += words[digit];

    }

    document.getElementById("result").innerHTML = result;

}