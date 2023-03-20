document.addEventListener('DOMContentLoaded', function() {

    // EDIT POST //

    document.querySelectorAll('.edit').forEach(function(editButton) {
      editButton.onclick = function() {
        // Get post id and retrieve original body of post
        const post_id = this.dataset.id;
        const postBody = document.querySelector(`#post-body-${post_id}`);
        const body = postBody.textContent;

        // Create a form element with a csrf token
        const form = document.createElement('form');
        const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        // fill this form element with the following html
        form.innerHTML = `
          <div class="form-group">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
            <textarea class="form-control" name="body" required>${body}</textarea>
            <button type="submit" class="btn btn-success mt-2">Save</button>
          </div>
        `;
        // replace original post body p element with form
        postBody.replaceWith(form);


        // When form is submitted
        form.onsubmit = function(event) {
          event.preventDefault();

          // get csrf token and updated new body of post
          const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
          const newBody = form.querySelector('textarea').value;

          // send put request to update database
          fetch(`/edit/${post_id}`, {
            method: 'PUT',
            headers: {
              'X-CSRFToken': csrfToken,
            },

            body: JSON.stringify({ body: newBody })
            })

            .then(response => response.arrayBuffer())
            .then(result => {
                postBody.textContent = newBody;
                form.replaceWith(postBody);
            });
        };
      };
    });


        // LIKE POST //

    if (isAuthenticated) {
        document.querySelectorAll('.glyphicon').forEach(function(hearticon) {
            hearticon.addEventListener('click', function() {

                // Get post id
                const post_id = this.dataset.like;
                const liked = this.dataset.liked;
                
                let like_count = parseInt(document.querySelector(`#like-count-${post_id}`).innerHTML)
                
                //console.log(like_count)
            
                // update post like count on server
                fetch(`/like/${post_id}`, {
                    method: 'PUT',
                    headers: {
                    'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    },
                    })

                    .then(response => {
                        // update heart icon
                        if (liked === "False") {
                            this.classList.remove("glyphicon-heart-empty");
                            this.classList.add("glyphicon-heart");
                            this.dataset.liked = "True";
                            like_count = like_count + 1;
                        } else {
                            this.classList.remove("glyphicon-heart");
                            this.classList.add("glyphicon-heart-empty");
                            this.dataset.liked = "False";
                            like_count = like_count - 1;
                        }  

                        // update like count
                        document.querySelector(`#like-count-${post_id}`).innerHTML = like_count;
                    })  
            }   )  
        })
    }   
});
  