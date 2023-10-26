const config_btn = document.querySelector("#config-btn");
const llm = document.querySelector("#llm");
const vector = document.querySelector("#vector");
// const temp = document.querySelector("#temp");

$(config_btn).on("click", () => {

    var u_llm = llm.options[llm.options.selectedIndex].value
    var u_temp = temp.value;
    var u_topK = topK.value;
    var u_vector = vector.options[vector.options.selectedIndex].value
    
    
});
