document.addEventListener('DOMContentLoaded', () => {

    /* ------------- EDIT FOR CLEANS ----------------- */

    document.querySelectorAll('.clean-edit-icon').forEach(function(button) {

        button.addEventListener('click', (event)=> {

            // Get Clean ID
            const cleanId = event.target.getAttribute('data-cleanid');
            console.log(cleanId)
 
            // Get relevant clean section
            const cleanSection = document.querySelector(`#clean-section-${cleanId}`)
            console.log(cleanSection)

            // Create a form element
            const div = document.createElement('div');

            const editCleanForm = `/minilogistic/editcleanform/${cleanId}/`;
            
            fetch(editCleanForm)
                .then(response => response.text())
                .then(html => {
                    div.innerHTML = html;
                    cleanSection.replaceWith(div);


                })

            
            

        }) 
  
    })


})