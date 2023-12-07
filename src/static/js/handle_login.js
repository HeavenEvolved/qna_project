$("#login_btn").on("click", (e) => {
    e.preventDefault();
    var email = $("#u_email").val();
    var pass = $("#u_pass").val();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.post(
        "",
        {
            email: email,
            pass: pass,
            csrfmiddlewaretoken: csrftoken,
        },
        (data) => {
            window.location = data.url;
            if (data.status == 1) {
                console.log(window);
            } else {
            }
        }
    );
});
