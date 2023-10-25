const dropZone = document.querySelector("#dropzone");
const dropMsg = document.querySelector("#error");
const dropInput = document.querySelector("#file_upload");

const permitted = ["pdf", "doc", "docx", "txt"];

function filterFiles(files) {
    var finalArray = [];

    for (let i = 0; i < files.length; i++) {
        if (permitted.includes(files[i].name.split(".")[1])) {
            if (files[i].size > 0 && files[i].size < 1000000000) {
                finalArray.push(files[i]);
            } else {
                dropMsg.textContent =
                    files[i].name +
                    " is too big! The Maximum File size is 1GB. The size of this file is " +
                    files[i].size +
                    ". Try again!";
                continue;
            }
        } else {
            dropMsg.textContent =
                files[i].name +
                " is not permitted! We only accept PDF, DOC, DOCX and TXT files. Try again!";
            continue;
        }

        setTimeout(() => {
            dropMsg.textContent = "Drag-n-Drop or Click to upload your files!";
        }, 500);
    }

    return finalArray;
}

$(dropZone).on("click", (e) => {
    dropInput.click();
    dropInput.onchange = (e) => {
        upload(filterFiles(e.target.files));
    };
});

$(dropZone).on("dragenter", (e) => {
    e.stopPropagation();
    e.preventDefault();
});

$(dropZone).on("dragover", (e) => {
    e.stopPropagation();
    e.preventDefault();
});

$(dropZone).on("drop", (e) => {
    e.preventDefault();
    upload(filterFiles(e.originalEvent.dataTransfer.files));
});

function upload(files) {
    for (let i = 0; i < files.length; i++) {
        var fd = new FormData();
        fd.append("file", files[i]);

        const csrftoken = $("[name=csrfmiddlewaretoken").val();

        var xhr = new XMLHttpRequest();

        xhr.addEventListener("progress", function (e) {
            var done = e.position || e.loaded;
            var total = e.totalSize || e.total;
            console.log(
                "xhr progress: " + Math.round((done / total) * 100) + "%"
            );
        });

        xhr.open("POST", "", true);
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.send(fd);
    }
}
