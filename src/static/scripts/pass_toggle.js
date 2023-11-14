$("#toggler").on("click", (e) => {
    e.preventDefault();
    $("#pass_toggle").toggleClass("bi-eye");

    // prettier-ignore
    if ($("#u_pass").attr("type") === "password") $("#u_pass").attr("type", "text");
    else $("#u_pass").attr("type", "password");
});
