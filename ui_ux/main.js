$(".user").hover(
    function () {
        // over
        $(".menu").addClass("active");
    },
    function () {
        // out
        $(".menu").removeClass("active");
    }
);

$("#temp").on("input", (e) => {
    $("#tempVal").text(e.target.value);
});

$(".llm-item>input").on("input", (e) => {
    
    if (e.target.id === "llama-2") $('#context').attr("max", "512").val("512");
    else if (e.target.id === "gpt-3_5") $('#context').attr("max", "4096").attr("min", "512").val("4096");
    else if (e.target.id === "gpt-4") $('#context').attr("max", "8192").attr("min", "512").val("8192");
    
    $("#contextVal").text($('#context').val());
});

$("#context").on("input", (e) => {
    if (e.target.value > 4096) e.target.value = 8192;
    else if (e.target.value > 2048) e.target.value = 4096;
    else if (e.target.value > 1024) e.target.value = 2048;
    else if (e.target.value > 512) e.target.value = 1024;

    $("#contextVal").text(e.target.value);
});
