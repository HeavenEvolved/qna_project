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

    const files = filterFiles(e.originalEvent.dataTransfer.files);

    upload(files);
});

function upload(files) {
    for (let i = 0; i < files.length; i++) {
        var fd = new FormData();
        fd.append("file", files[i]);

        dropMsg.textContent = "Uploading...";

        const req = new XMLHttpRequest();
        req.open("POST", "");

        req.upload.addEventListener("progress", (e) => {
            const progress = e.loaded / e.total;
            dropMsg.textContent = (progress * 100).toFixed() + "%";

            if (progress === 1) dropMsg.textContent = "Processing...";
        });

        req.addEventListener("load", () => {
            if (req.status === 200) {
                dropMsg.textContent = "Success!";
                console.log(JSON.parse(req.responseText));
            }
            else {
                dropMsg.textContent = "Upload Failed!";
            }
        });

        req.addEventListener("error", () => {
            dropMsg.textContent = "Upload failed!";
        })

        req.send(fd);
    }
}
