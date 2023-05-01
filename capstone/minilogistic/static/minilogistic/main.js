document.addEventListener("DOMContentLoaded", () => {
    const datePicker = document.querySelector("#datepicker");
    const fulldatePicker = document.querySelector("#fulldatepicker");
    const agendaBody = document.querySelector("#agenda-body");
    const fulldayAgendaBody =document.querySelector("#fullday-agenda-body");
    const horizontalToggle = document.querySelector("#horizontal");
    
    

    // ----------- DATEPICKER ---------------- // 
    function updateView(date, toggle) {
    
        agendaBody.style.opacity = 0; // make old days go away smoothly using css transition

        fetch(`/minilogistic/days?selected=${date}&horizontal=${toggle}`)
            .then((response) => response.text())
            .then((rendered_day_section) => {
                setTimeout(() => {
                    
                    agendaBody.innerHTML = rendered_day_section; // Add new days to inner HTML
    
                    agendaBody.style.opacity = 1; // make new days appear smoothly with css transition
    
                    createEventListeners(); // Re-apply all event listeners
                    
                }, 500); // Delay 500ms before adding new days
            })
            .catch((error) => console.error(error));
            

    }


    /* -------- FULLDAY DATEPICKER ----------- */

    function updateFullday(date) {

        // Update the URL 
        const newUrl = `/minilogistic/fullday/${date}/`
        window.history.pushState(null, '', newUrl)

        fulldayAgendaBody.style.opacity = 0; // make old day go away smoothly using css transition

        fetch(`/minilogistic/fulldaybody?selected=${date}`)
            .then((response) => response.text())
            .then((rendered_fullday_section) => {
                
                setTimeout(() => {
                    fulldayAgendaBody.innerHTML = rendered_fullday_section; // Add new day to inner HTML
    
                    fulldayAgendaBody.style.opacity = 1; // make new day appear smoothly with css transition
    
                    createEventListeners(); // Re-apply all event listeners
                    
                }, 500); // Delay 500ms before adding new day
            })
            .catch((error) => console.error(error));
    }


    // ------------------------------------------ //
    // Define function to create event listeners  //
    // ------------------------------------------ //

    function createEventListeners() {

        

        // --------------------------------------------- //
        // ----------- Date Picker Event -------------- //
        
            document.addEventListener("input", (event) => {  

                if (event.target.matches("#datepicker")) {
                    if (horizontalToggle) {
                        const datePicker = event.target;
                        if (datePicker) {
                            const date = datePicker.value
                            const toggle = horizontalToggle.checked;
                    
                            updateView(date, toggle);
                        }
                        
                    }
                
                }
            });

        // --------------------------------------------- //
        // -------- Fullday Date Picker Event ---------- //


            if (fulldatePicker) {
                fulldatePicker.addEventListener("input", () => {
                    date = fulldatePicker.value
                    updateFullday(date);
                })
            }
        
        // --------------------------------------------- //
        // ------------ Horizontal Toggle -------------- //

         
        document.addEventListener("change", (event) => {
            if (event.target.matches("#horizontal")) { // Check if page has toggle

                const horizontalToggle = event.target
                const toggle = horizontalToggle.checked;
                const date = document.querySelector("#datepicker").value;
                //console.log('toggle value:', toggle); 

                const url = '/minilogistic/update-toggle/';
                const data = { toggle: toggle };
                // console.log('data:', data); 
            
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(data)
                })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error("Error updating toggle.");
                    }
                })
                .then(data => {
                    console.log(data); 
            
                    // Refresh the front-end view with updated toggle value
                    updateView(date, toggle);
                })
                .catch(error => console.error(error));


            }
            
        });


        // --------------------------------------------- //
        // ---------------- Booking Form --------------- //

        // Display the form
        document.querySelectorAll('.booking-button').forEach((button) => { 
            button.addEventListener('click', (event) => {   // attach event listeners to all "ADD BOOKING" buttons
                var bookingFormUrl = event.target.getAttribute('data-booking-form-url');

                
                fetch(bookingFormUrl)
                    .then(response => response.text())
                    .then(html => {
                        // Find form-container element within the same day-section as the clicked button
                        var formContainer = event.target.closest('.day-section').querySelector('.form-container');
                        // Make space for form
                        formContainer.style.maxHeight = "500px";
                        // Add the form
                        formContainer.innerHTML = html;
        
                       
                        // Set the arrival date on the form to the date of the selected day-section
                        var sectionDate = event.target.closest('.day-section').querySelector('.section-date').dataset.date;
                        var checkInInput = formContainer.querySelector('#arrival-date');
                        checkInInput.value = sectionDate;

                        
                        attachColorButtonListeners(); // Add color event listeners


                        // Make form disappear when .cancel-form is clicked
                        var cancelFormButton = formContainer.querySelector('.cancel-form');
                        cancelFormButton.addEventListener('click', () => {
                            
                            formContainer.style.opacity = "0";
                            formContainer.style.maxHeight = "0";
        
                            setTimeout(() => {
                                
        
                                cleanButtons.forEach((btn) => (btn.style.opacity = 1));
                                bookingButtons.forEach((btn) => (btn.style.opacity = 1));
                            }, 600); 
        
                            setTimeout(() => {
                                formContainer.innerHTML = '';
                            }, 700); 
                                
                        });

                        // Attach the submit event listener to the new form
                        const newForm = formContainer.querySelector('.add-new-item-form');
                        newForm.addEventListener('submit', handleFormSubmit);
                        
                    })
                    .catch(error => console.error(error));
            });
        });
        

        // Hide (Add Clean) and (Add Booking) buttons when booking form is opened //

        const bookingButtons = document.querySelectorAll('.booking-button');
        const cleanButtons = document.querySelectorAll('.clean-button');
        
        
        bookingButtons.forEach((button) => {
            button.addEventListener('click', function (event) {

            const formContainer = event.target.closest('.day-section').querySelector('.form-container');
            formContainer.style.opacity = 1;
        
            cleanButtons.forEach((btn) => (btn.style.opacity = 0));
            bookingButtons.forEach((btn) => (btn.style.opacity = 0));
        
            });
        });
        
       
        // --------------------------------------------- //
        // -------------- New Clean Form --------------- //       Note: I can probably make Booking Form and New Clean Form sections from the same code.. Alot of repetition here...

        // Display form
        document.querySelectorAll('.clean-button').forEach((button) => {
            button.addEventListener('click', (event) => {  // attach event listeners to all "ADD CLEAN" buttons
                var newcleanFormUrl = event.target.getAttribute('data-newclean-form-url');

                
                fetch(newcleanFormUrl)
                    .then(response => response.text())
                    .then(html => {
                        // Find form-container element within the same day-section as the clicked button
                        var formContainer = event.target.closest('.day-section').querySelector('.form-container');
                        // Make space for form
                        formContainer.style.maxHeight = "500px"; 
                        // Add the form
                        formContainer.innerHTML = html;
                        // Extract the date value from section-date element
                        var sectionDate = event.target.closest('.day-section').querySelector('.section-date').dataset.date;
                        

                        // Set the value of the clean date input field with the extracted date value
                        var cleanDateInput = formContainer.querySelector('#clean-date');
                        cleanDateInput.value = sectionDate;

                        // Add color event listeners
                        attachColorButtonListeners();

                        // Make form disappear when cancel-form is clicked
                        var cancelFormButton = formContainer.querySelector('.cancel-form');
                        cancelFormButton.addEventListener('click', () => {
                            
                            formContainer.style.opacity = "0";
                            formContainer.style.maxHeight = "0";
        
                            setTimeout(() => {
                                formContainer.innerHTML = '';
        
                                cleanButtons.forEach((btn) => (btn.style.opacity = 1));
                                bookingButtons.forEach((btn) => (btn.style.opacity = 1));
                            }, 600); 
        
                            setTimeout(() => {
                                formContainer.innerHTML = '';
                            }, 700); 
                                
                        });

                        // Attach the submit event listener to the new form
                        const newForm = formContainer.querySelector('.add-new-item-form');
                        newForm.addEventListener('submit', handleFormSubmit);
 
                    })
                    .catch(error => console.error(error));
            });
        });

        
        // Hide (Add Clean) and (Add Booking) buttons when new clean form is opened //
        cleanButtons.forEach((button) => {
            button.addEventListener('click', function (event) {
            const formContainer = event.target.closest('.day-section').querySelector('.form-container');
            formContainer.style.opacity = 1;
        
            cleanButtons.forEach((btn) => (btn.style.opacity = 0));
            bookingButtons.forEach((btn) => (btn.style.opacity = 0));
        
            
            });
        });


        // ----------------------------------------------------- //
        // ----------- When forms are submitted ----------------//
        
        function handleFormSubmit(event) {

            event.preventDefault();
            event.stopImmediatePropagation();
           
            const form = event.target;

            if (!form.classList.contains("add-new-item-form")) {

                console.log("Wrong form!!!")
                return;
            }

            let date;
            if (datePicker) {
                date = datePicker.value
            }
            else if (fulldatePicker) {
                date = fulldatePicker.value
            }
            let toggle;
            if (horizontalToggle) {
                toggle = horizontalToggle.checked;
            }
            console.log("date selected:", date)


            // ---- BOOKING FORM SUBMIT ---- //

            if (form.matches("#booking-form")) {
                const formData = new FormData(form);
                console.log("form matches Booking FOrm")

                
        
                // POST the data to the server
                fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                })
                    .then((response) => {
                        if (response.ok) {
                            if (datePicker) {
                                console.log("datePicker conditon triggered")
                                // Refresh the front-end view 
                                updateView(date, toggle)
                            }
                            else if (fulldatePicker) {
                                console.log("FulldatePicker condition trig")
                                console.log("date:", date)
                                // Refresh the front-end view 
                                updateFullday(date)
                            }
                            
                        } else {
                            throw new Error("Error adding booking.");
                        }
                    })
                    .catch((error) => console.error(error));
            }


            // ---- CLEAN FORM SUBMIT ---- //
        
            if (form.matches("#newclean-form")) {

                const formData = new FormData(form);
                console.log("form matches Clean FOrm")

                let date;
                if (datePicker) {
                    date = datePicker.value
                }
                else if (fulldatePicker) {
                    date = fulldatePicker.value
                }
                let toggle;
                if (horizontalToggle) {
                    toggle = horizontalToggle.checked;
                }

                console.log(formData)
        
                // POST the data to the server
                fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                })
                    .then((response) => {
                        if (response.ok) {
                            if (datePicker) {
                                console.log("datePicker conditon triggered")
                                // Refresh the front-end for agenda view
                                updateView(date, toggle)
                            }
                            else if (fulldatePicker) {
                                console.log("FulldatePicker condition triggered")
                                // Refresh the front-end view for fullday view
                                updateFullday(date)
                            }
                        } else {
                            throw new Error("Error adding clean.");
                        }
                    })
                    .catch((error) => console.error(error));
            } 

           

        };


        // --------------------------- EDIT SECTION ----------------------------------- //
    
       
        /* ------------- MAKE EDIT FORM FOR BOOKING APPEAR FILLED IN ----------------- */
       
        
        
        document.querySelectorAll('.booking-edit-icon').forEach(function(button) {

        
            button.addEventListener('click', (event)=> {

                console.log("booking-edit-icon clicked");
    
                // Get Clean ID
                const bookingId = event.target.getAttribute('data-bookingid');
                
                console.log(bookingId)
    
                // Get relevant clean section
                const bookingSection = document.querySelector(`#booking-section-${bookingId}`)
                console.log(bookingSection)
    
                // Create a form element
                const editDiv = document.createElement('div');
    
                const editBookingForm = `/minilogistic/editbookingform/${bookingId}/`;
                
                fetch(editBookingForm)
                    .then(response => response.text())
                    .then(html => {
                        editDiv.innerHTML = html;
                        bookingSection.replaceWith(editDiv);
    
                        // Attach color event listeners
                        attachColorButtonListeners();

                        // Attach the submit event listener to the new form
                        const newEditForm = document.querySelector('#edit-booking-form');
                        newEditForm.addEventListener('submit', handleEditFormSubmit);

                        // DELETE BUTTON
                        var deleteBookingButton = editDiv.querySelector('.delete-booking')
                        deleteBookingButton.addEventListener('click', () => {
                            let isConfirmed = confirm("Are you sure you want to delete this Booking?");

                            if (isConfirmed) {
                                deleteItem("booking", bookingId);
                            }
                            
                        })

                        // DELETE COMMENT
                        editDiv.querySelectorAll('.delete-comment').forEach(function(button) {

                            button.addEventListener('click', () => {
                                var commentId = button.dataset.commentid;
                                console.log("comment Id:", commentId)

                                let isConfirmed = confirm("Are you sure you want to delete this comment?");

                                if (isConfirmed) {
                                    deleteComment(commentId);
                                }
                                
                            })
                        });


                        // CANCEL FORM BUTTON (Not working)
                        var cancelFormButton = editDiv.querySelector('.cancel-form');
                        cancelFormButton.addEventListener('click', () => {
                            
                        
                            editDiv.style.opacity = "0";
                            editDiv.style.maxHeight = "0";

                            editDiv.replaceWith(bookingSection);
        
                            setTimeout(() => {
                                editDiv.innerHTML = '';
        
                                cleanButtons.forEach((btn) => (btn.style.opacity = 1));
                                bookingButtons.forEach((btn) => (btn.style.opacity = 1));
                            }, 600); 
            
                        });  
    
                    }) 
                    .catch(error => console.error(error));

            }) 
        })
    
        /* ------------- MAKE EDIT FORM FOR CLEAN APPEAR FILLED IN ----------------- */
       
        
    
            document.querySelectorAll('.clean-edit-icon').forEach(function(button) {
        
                button.addEventListener('click', (event)=> {
                    console.log("clean-edit-icon clicked");
        
                    // Get Clean ID
                    const cleanId = event.target.getAttribute('data-cleanid');
                    
                    console.log(cleanId)
        
                    // Get relevant clean section
                    const cleanSection = document.querySelector(`#clean-section-${cleanId}`)
                    console.log(cleanSection)
        
                    // Create a form element
                    const editDiv = document.createElement('div');
        
                    const editCleanForm = `/minilogistic/editcleanform/${cleanId}/`;
                    
                    fetch(editCleanForm)
                        .then(response => response.text())
                        .then(html => {
                            editDiv.innerHTML = html;
                            cleanSection.replaceWith(editDiv);
        
        
                            attachColorButtonListeners();

                            // Attach the submit event listener to the new form
                            const newEditForm = document.querySelector('#edit-clean-form');
                            newEditForm.addEventListener('submit', handleEditFormSubmit);

                            // DELETE BUTTON
                            var deleteCleanButton = editDiv.querySelector('.delete-clean')
                            deleteCleanButton.addEventListener('click', () => {
                                let isConfirmed = confirm("Are you sure you want to delete this clean?");

                                if (isConfirmed) {
                                    deleteItem("clean", cleanId);
                                }
                                
                            })

                            // DELETE COMMENT
                            editDiv.querySelectorAll('.delete-comment').forEach(function(button) {

                                button.addEventListener('click', () => {
                                    var commentId = button.dataset.commentid;
                                    console.log("comment Id:", commentId)

                                    let isConfirmed = confirm("Are you sure you want to delete this comment?");

                                    if (isConfirmed) {
                                        deleteComment(commentId);
                                    }
                                    
                                })
                            });


                            // CANCEL FORM BUTTON (Not working)
                            var cancelFormButton = editDiv.querySelector('.cancel-form');
                            cancelFormButton.addEventListener('click', () => {
                                
                            
                                editDiv.style.opacity = "0";
                                editDiv.style.maxHeight = "0";

                                editDiv.replaceWith(cleanSection);
            
                                setTimeout(() => {
                                    editDiv.innerHTML = '';
            
                                    cleanButtons.forEach((btn) => (btn.style.opacity = 1));
                                    bookingButtons.forEach((btn) => (btn.style.opacity = 1));
                                }, 600);
                                
                            });
                        })
                        .catch(error => console.error(error)); 
                }) 
            })


        // ----------------------- DELETE FUNCTION -------------------------- //

        function deleteItem(item, id) {

            let date;
            if (datePicker) {
                date = datePicker.value
            }
            else if (fulldatePicker) {
                date = fulldatePicker.value
            }
            let toggle;
            if (horizontalToggle) {
                toggle = horizontalToggle.checked;
            }

            const deleteCleanUrl = `/minilogistic/delete${item}/${id}/`;

            fetch(deleteCleanUrl)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    if (data.status === "success") {
                        console.log("Success condition triggered");
                        // Perform any actions on successful form submission, e.g., show a success message
                        if (datePicker) {
                            console.log("datePicker conditon triggered")
                            // Refresh the front-end view 
                            updateView(date, toggle)
                            
                        }
                        else if (fulldatePicker) {
                            console.log("FulldatePicker condition triggered")
                            // Refresh the front-end view 
                            updateFullday(date)
                            
                        }
                    } else {
                        // Handle any error messages here
                        console.error("Error:", data.message);
                    }
                })
                .catch(error => console.error(error));

        }


        // ----------------------- DELETE COMMENT FUNCTION -------------------------- //

        function deleteComment(comment) {


            const deleteCommentUrl = `/minilogistic/deletecomment/${comment}/`;
            const commentContainer = document.querySelector(`.comment-container-${comment}`)

            fetch(deleteCommentUrl)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    if (data.status === "success") {
                        console.log("Success condition triggered");
                        // Make comment dissapear
                        commentContainer.remove();
                        
                    } else {
                        // Handle any error messages here
                        console.error("Error:", data.message);
                    }
                })
                .catch(error => console.error(error));

        }
    
        /* ------------- EDIT FORM SUBMISSION ----------------- */
    
        
        function handleEditFormSubmit(event) {
            
            event.preventDefault();
            event.stopImmediatePropagation();
        
            const form = event.target;
        
            const formData = new FormData(form);

                let date;
                if (datePicker) {
                    date = datePicker.value
                }
                else if (fulldatePicker) {
                    date = fulldatePicker.value
                }
                let toggle;
                if (horizontalToggle) {
                    toggle = horizontalToggle.checked;
                }
        
            // POST the data to the server
            fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                if (data.status === "success") {
                    console.log("Success condition triggered");
                    
                    if (datePicker) {
                        console.log("datePicker conditon triggered")
                        // Refresh agenda view
                        updateView(date, toggle)
                        
                    }
                    else if (fulldatePicker) {
                        console.log("FulldatePicker condition triggered")
                        // Refresh fullday view
                        updateFullday(date)

                    }
                } else {
                    console.error("Error:", data.message);
                }
            })
            .catch(error => console.error(error));
        };
        
    
    
    
        // -------- Comment color event listeners --------- //

        function setColor(input, color) {
            input.value = color;
        }
        
        function attachColorButtonListeners() {
            document.querySelectorAll('#comment-color').forEach((input) => {
                var formElement = input.closest('.row');
                var buttons = formElement.querySelectorAll('.btn-group button');
        
                buttons.forEach((button) => {
                    button.addEventListener('click', () => {
                        console.log("Color button clicked")
                        var color = button.getAttribute('data-color');
                        setColor(input, color);
                    });
                });
            });
        }

        // ------------------------------------------------------------------------------ //

        


    }

    //Add arrival time field to new clean form when "Same day ?" is selected
    document.addEventListener("change", function (event) {
        if (event.target.matches("input[type='checkbox']#same-day")) {
            const sameDayCheckbox = event.target;
            const arrivalTimeContainer = document.querySelector("#clean-form-arrival-time-container");

            if (sameDayCheckbox.checked) {
                arrivalTimeContainer.style.display = "block";
            } else {
                arrivalTimeContainer.style.display = "none";
            }
        }
    });


    //-------- FOR CSRF TOKEN VALIDATION ----------------------- //

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
    

    createEventListeners();
    

});
