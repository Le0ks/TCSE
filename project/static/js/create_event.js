const typeByTimeField = document.getElementById("id_event-type_by_time");
typeByTimeField.addEventListener("change", updateForm);
updateForm({target: typeByTimeField});


function addAnswer(id) {
    const block = document.getElementById(`answers-${id}`);
    const newEl = block.lastElementChild.cloneNode(true);
    newEl.querySelector("textarea").style = "";
    newEl.innerHTML = newEl.innerHTML.replaceAll(`answers-${id}-${block.children.length - 1}`, `answers-${id}-${block.children.length}`).replace(`Ответ ${block.children.length}`, `Ответ ${block.children.length + 1}`).replace(`Комментарий к ответу ${block.children.length}`, `Комментарий к ответу ${block.children.length + 1}`);
    newEl.querySelector("textarea").addEventListener("keydown", autosize);
    block.appendChild(newEl);
    document.getElementById(`id_answers-${id}-TOTAL_FORMS`).value = block.children.length;
}

function addTask() {
    const block = document.getElementById("tasks");
    const newEl = block.lastElementChild.cloneNode(true);
    let newId = block.children.length - 4;
    newEl.className = newEl.className.replace(`task_form-${newId}`, `task_form-${newId + 1}`);
    newEl.querySelector("button").setAttribute("data-id", newId + 1);
    newEl.querySelector("button").setAttribute("onclick", `addAnswer(${newId + 1})`);
    let answers = newEl.querySelector(`#answers-${newId}`);
    while (answers.children.length > 2) {
        answers.removeChild(answers.lastChild);
    }
    newEl.innerHTML = newEl.innerHTML.replace(`Задание ${newId}`, `Задание ${newId + 1}`).replaceAll(`tasks-${newId - 1}`, `tasks-${newId}`).replaceAll(`answers-${newId}`, `answers-${newId + 1}`);
    for (let textarea of newEl.querySelectorAll("textarea")) {
        textarea.addEventListener("keydown", autosize);
    }
    block.appendChild(newEl);
    document.getElementById(`id_tasks-TOTAL_FORMS`).value = newId + 1;
}


var textareas = document.querySelectorAll("textarea");

for (var i = 0; i < textareas.length; i++) {
    textareas[i].addEventListener("keydown", autosize);
}

function autosize(){
  var el = this;
  setTimeout(function(){
    el.style.cssText = "height: 1rem";
    el.style.cssText = "height:" + el.scrollHeight + "px !important";
  }, 0);
}

function deleteAnswer(element) {
    let answers = element.parentElement.parentElement.parentElement;
    let answersID = answers.id;
    if (answers.children.length == 1) {
        return
    }
    answers.parentElement.querySelector(`input[name="${answersID}-TOTAL_FORMS"]`).value--;
    let answer = element.parentElement.parentElement;
    let index = Array.from(answers.children).indexOf(answer);
    answer.remove();
    for (let i = index; i < answers.children.length; i++) {
        answers.children[i].innerHTML = answers.children[i].innerHTML.replaceAll(`${answersID}-${i + 1}`, `${answersID}-${i}`).replace(`Ответ ${i + 2}`, `Ответ ${i + 1}`).replace(`Комментарий к ответу ${i + 2}`, `Комментарий к ответу ${i + 1}`);
        console.log(answers.children[i]);
    }
}

function deleteTask(element) {
    let tasks = element.parentElement.parentElement.parentElement;
    if (tasks.children.length - 4 == 1) {
        return
    }
    tasks.querySelector("input[name='tasks-TOTAL_FORMS']").value--;
    let task = element.parentElement.parentElement;
    let index = Array.from(tasks.children).indexOf(task) - 4;
    task.remove();
    for (let i = index + 4; i < tasks.children.length; i++) {
        tasks.children[i].className = tasks.children[i].className.replace(`task_form-${index + 2}`, `task_form-${index + 1}`);
        tasks.children[i].querySelector("button").setAttribute("data-id", index + 1);
        tasks.children[i].querySelector("button").setAttribute("onclick", `addAnswer(${index + 1})`);
        let answers = tasks.children[i].querySelector(`#answers-${index + 1}`);
        tasks.children[i].innerHTML = tasks.children[i].innerHTML.replace(`Задание ${index + 2}`, `Задание ${index + 1}`).replaceAll(`tasks-${index + 1}`, `tasks-${index}`).replaceAll(`answers-${index + 2}`, `answers-${index + 1}`);
    }
}
