let tasks = [
    
];

displayTasks();

function displayTasks(){

    let html = "";
    let completed = 0;

    for(let i=0;i<tasks.length;i++){

        if(tasks[i].done) completed++;

        html += `
        <div class="task">
            <div class="${tasks[i].done ? "done":""}"
                 onclick="toggleTask(${i})">
                 ${tasks[i].name}
            </div>

            <span onclick="deleteTask(${i})">×</span>
        </div>`;
    }

    document.getElementById("taskList").innerHTML = html;

    document.getElementById("count").innerHTML =
    `${completed} of ${tasks.length} tasks done`;
}

function addTask(){

    let input = document.getElementById("taskInput");

    if(input.value.trim()=="") return;

    tasks.push({
        name:input.value,
        done:false
    });

    input.value="";

    displayTasks();
}

function deleteTask(index){

    tasks.splice(index,1);

    displayTasks();
}

function toggleTask(index){

    tasks[index].done = !tasks[index].done;

    displayTasks();
}

document.getElementById("taskInput").addEventListener("keypress",function(e){

    if(e.key==="Enter"){
        addTask();
    }

});