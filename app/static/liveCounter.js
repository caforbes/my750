const formArea = document.getElementById("entry-form");

function wordCount(text) {
    return text.split(/\s+/).filter(item => !!item ).length;
}

function displayWordCount(e) {
    let text = e.target.value;
    let count = wordCount(text);
    let countMeetsGoal = count >= 750;
    // update wordcount text
    const counter = document.querySelector('.wordcount-display');
    counter.textContent = count;
    // update progressbar percentage and styling
    const progBar = document.querySelector('.progress');
    progBar.value = count;
    if (countMeetsGoal && !progBar.classList.contains('is-success')) {
        progBar.classList.remove('is-info');
        progBar.classList.add('is-success');
    } else if (!countMeetsGoal && progBar.classList.contains('is-success')) {
        progBar.classList.remove('is-success');
        progBar.classList.add('is-info');
    }
}


formArea.addEventListener("input", displayWordCount)