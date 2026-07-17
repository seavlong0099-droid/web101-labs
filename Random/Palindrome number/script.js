function checkPalindrome(){

    let number = document.getElementById("numberInput").value;

    let reverse = "";


    // reverse the number
    for(let i = number.length - 1; i >= 0; i--){

        reverse += number[i];

    }


    // check palindrome
    if(number == reverse){

        document.getElementById("result").innerHTML =
        number + " is a palindrome number";

    }
    else{

        document.getElementById("result").innerHTML =
        number + " is not a palindrome number";

    }

}