function formatTime(seconds) {

    if (seconds < 0) {
        seconds = 0;
    }

    const hrs = Math.floor(seconds / 3600);

    const mins = Math.floor((seconds % 3600) / 60);

    const secs = seconds % 60;

    return (
        String(hrs).padStart(2, "0") + ":" +
        String(mins).padStart(2, "0") + ":" +
        String(secs).padStart(2, "0")
    );

}


function updateTimers() {

    document.querySelectorAll(".live-timer").forEach(function(timer){

        const started = timer.dataset.started;

        const completed = timer.dataset.completed;

        const status = timer.dataset.status;

        if(!started){

            timer.textContent = "--:--:--";

            return;

        }

        const startedTime = new Date(started);

        if(isNaN(startedTime.getTime())){

            timer.textContent = "--:--:--";

            return;

        }

        let endTime;

        if(status === "Completed" && completed){

            endTime = new Date(completed);

        }else{

            endTime = new Date();

        }

        const seconds = Math.floor(
            (endTime.getTime() - startedTime.getTime()) / 1000
        );

        timer.textContent = formatTime(seconds);

        // Reset colors
        timer.style.fontWeight = "bold";
        timer.style.color = "";

        // Completed requests
        if(status === "Completed"){

            timer.style.color = "green";

        }

        // 1 hour warning
        else if(seconds >= 3600){

            timer.style.color = "red";

        }

    });

}

updateTimers();

const timerInterval = setInterval(() => {

    updateTimers();

    const runningTimers = document.querySelectorAll(
        '.live-timer[data-status="In Progress"]'
    );

    if (runningTimers.length === 0) {
        clearInterval(timerInterval);
    }

}, 1000);