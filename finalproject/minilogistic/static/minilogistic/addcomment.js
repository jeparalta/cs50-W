 
 // --------------- ADD COMMENT ------------------- //
 document.addEventListener("DOMContentLoaded", () => {

        document.querySelectorAll('.submit-comment-button').forEach((button) => {
            button.addEventListener('click', (event)=> {

                //console.log("Comment button clicked") 

                

                const form = event.target.closest("form");
                const formData = new FormData(form)

                console.log(formData)

                const commentBody = form.querySelector("#comment-body");
                if (commentBody.value.trim() === "") {
                    event.preventDefault();
                    alert("New Comment field cannot be empty.");
                    return;
                }

                //event.preventDefault();
                //event.stopImmediatePropagation();

                console.log("Form data:", Array.from(formData.entries()));

                fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                })
                .then((response) => response.json())
                .then((data) => {
                    if (data.status === "success") {
                        form.elements["comment_body"].value = "";

                        const newComment = JSON.parse(data.comment)[0];

                        const li = document.createElement("li");
                        li.textContent = newComment.fields.body;

                        const div = document.createElement("div");
                        div.className = newComment.fields.clean_belong ? 'clean-comment-container' : 'booking-comment-container';

                        div.appendChild(li)

                        const comment_list = form.closest("div.row").previousElementSibling.querySelector(".comments-section ul");

                        setTimeout(() => {
                        comment_list.appendChild(div);
                        }, 500);
                    }
                    else {
                        throw new Error ("Error adding new comment.");
                    }
                })
                .catch((error) => console.error(error));

            })
        }); 




        // -------- FOR CSRF TOKEN VALIDATION ----------------------- //

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split("; ");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

})
