var temp = document.querySelector("#temp");
var tempVal = document.querySelector("#tempVal");

var topK = document.querySelector("#topK");
var kVal = document.querySelector("#kVal");

$(document).ready(() => {
    $(tempVal).text(temp.value);
    $(tempVal).removeClass("hidden");

    $(kVal).text(topK.value);
    $(kVal).removeClass("hidden");
});

$(temp).on("input", (e) => {
    $(tempVal).text(e.target.value);
});

$(topK).on("input", (e) => {
    $(kVal).text(e.target.value);
});
