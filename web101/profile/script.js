function toggleInfo(){

    let info = document.getElementById("moreInfo");
    let btn = document.getElementById("btn");

    if(info.style.display === "none"){

        info.style.display = "block";
        btn.innerHTML = "Show Less";

    }else{

        info.style.display = "none";
        btn.innerHTML = "Show More";

    }

}