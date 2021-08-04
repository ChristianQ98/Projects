var sliderHappy = document.getElementById("overall_happiness");
var outputHappy = document.getElementById("happiness");
outputHappy.innerHTML = sliderHappy.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
sliderHappy.oninput = function () {
    outputHappy.innerHTML = this.value;
}



var sliderProductive = document.getElementById("overall_productivity");
var outputProductive = document.getElementById("productivity");
outputProductive.innerHTML = sliderProductive.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
sliderProductive.oninput = function () {
    outputProductive.innerHTML = this.value;
}