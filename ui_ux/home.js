var links = document.querySelectorAll("a");

var list_button = document.querySelectorAll(".list-item");
var option_button = document.querySelectorAll(".option");

if (links) {
    links.forEach((link) => {
        link.addEventListener("click", () => {
            $("." + link.classList[0] + ".selected").removeClass("selected");
            $(link).addClass("selected");
        });
    });
}
