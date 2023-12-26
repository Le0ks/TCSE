function updateForm(event) {
    const formValue = event.target.value;
    const startTimeField = document.getElementById("id_event-start_time");
    const finishTimeField = document.getElementById("id_event-finish_time");
    const durationField = document.getElementById("id_event-duration");
    
    const startTimeLabel = document.getElementById("id_event-start_time-label");
    const finishTimeLabel = document.getElementById("id_event-finish_time-label");
    const durationLabel = document.getElementById("id_event-duration-label");

    startTimeField.parentElement.style.display = "none";
    startTimeField.required = false;
    finishTimeField.parentElement.style.display = "none";
    finishTimeField.required = false;
    durationField.parentElement.style.display = "none";
    durationField.required = false;

    startTimeLabel.style.display = "none";
    finishTimeLabel.style.display = "none";
    durationLabel.style.display = "none";

    if (formValue == 1) {
        durationField.parentElement.style.display = "block";
        durationField.required = true;
        durationLabel.style.display = "block";
    } else if (formValue == 2) {
        startTimeField.parentElement.style.display = "block";
        startTimeField.required = true;
        finishTimeField.parentElement.style.display = "block";
        finishTimeField.required = true;
        startTimeLabel.style.display = "block";
        finishTimeLabel.style.display = "block";
    } else if (formValue == 3) {
        startTimeField.parentElement.style.display = "block";
        startTimeField.required = true;
        finishTimeField.parentElement.style.display = "block";
        finishTimeField.required = true;
        durationField.parentElement.style.display = "block";
        durationField.required = true;
        durationLabel.style.display = "block";
        startTimeLabel.style.display = "block";
        finishTimeLabel.style.display = "block";
    }
}
