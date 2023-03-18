document.addEventListener('DOMContentLoaded', function() {
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
  });
  