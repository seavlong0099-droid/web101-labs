function generateTable(){

    let num = document.getElementById("number").value;
    let tbody = document.querySelector("#table tbody");

    tbody.innerHTML = "";

    if(num === ""){
        alert("Please enter a number.");
        return;
    }

    for(let i = 1; i <= 10; i++){

        let row = `
            <tr>
                <td>${num} x ${i}</td>
                <td>${num * i}</td>
            </tr>
        `;

        tbody.innerHTML += row;
    }
}