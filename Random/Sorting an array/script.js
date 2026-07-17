function sortArray(){

    // Get input from user
    let input = document.getElementById("arrayInput").value;


    // Convert string to array
    let arr = input.split(",");


    // Convert string numbers to integer
    for(let i = 0; i < arr.length; i++){

        arr[i] = Number(arr[i]);

    }


    // Bubble Sort (without sort())
    for(let i = 0; i < arr.length; i++){

        for(let j = 0; j < arr.length - 1; j++){

            if(arr[j] > arr[j + 1]){

                let temp = arr[j];

                arr[j] = arr[j + 1];

                arr[j + 1] = temp;

            }

        }

    }


    // Display result
    document.getElementById("result").innerHTML = arr;

}