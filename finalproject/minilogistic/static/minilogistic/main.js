document.addEventListener("DOMContentLoaded", () => {
    const datePicker = document.querySelector("#datepicker");
    const fulldatePicker = document.querySelector("#fulldatepicker");
    /*const daySectionContainer = document.querySelector(".day-section-container");*/
    const agendaBody = document.querySelector("#agenda-body");
    const fulldayAgendaBody =document.querySelector("#fullday-agenda-body");
    const horizontalToggle = document.querySelector("#horizontal");
    

    // ----------- DATEPICKER ---------------- //
    function updateView(date, toggle) {
        // const date = datePicker.value; // get new date selected on date picker
    
        agendaBody.style.opacity = 0; // make old days go away smoothly using css transition
        fetch(`/minilogistic/days?selected=${date}&horizontal=${toggle}`)
            .then((response) => response.text())
            .then((rendered_day_section) => {
                setTimeout(() => {
                    
                    agendaBody.innerHTML = rendered_day_section;
    
                    agendaBody.style.opacity = 1; // make new days appear smoothly with css transition
    
                    createEventListeners(); // Initialize event listeners for the new day-sections Add buttons to open forms
                    
                }, 500); // Wait for 500ms before updating the content and making it visible again
            })
            .catch((error) => console.error(error));
            

    }


    /* -------- FULLDAY DATEPICKER ---------------------- NEEDS WORK!!!! */

    function updateFullday(date) {

        //const date = fulldatePicker.value; // get new date selected on date picker
        console.log("Fulldate picker value:", date)

        // Update the URL 
        const newUrl = `/minilogistic/fullday/${date}/`
        window.history.pushState(null, '', newUrl)

        fulldayAgendaBody.style.opacity = 0; // make old days go away smoothly using css transition
        fetch(`/minilogistic/fulldaybody?selected=${date}`)
            .then((response) => response.text())
            .then((rendered_fullday_section) => {
                
                setTimeout(() => {
                    fulldayAgendaBody.innerHTML = rendered_fullday_section;
    
                    fulldayAgendaBody.style.opacity = 1; // make new days appear smoothly with css transition
    
                    createEventListeners(); // Initialize event listeners for the new day-sections Add buttons to open forms
                    
                }, 500); // Wait for 500ms before updating the content and making it visible again
            })
            .catch((error) => console.error(error));
    }

    if (fulldatePicker) {
        fulldatePicker.addEventListener("input", () => {
            date = fulldatePicker.value
            updateFullday(date);
        })
    }



    // ------------------------------------------------------------------------ //
    // Define function to create event listeners for Add buttons to open forms  //
    // ------------------------------------------------------------------------ //

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
        // ------------ Horizontal Toggle -------------- //

         // Check if page has toggle
        document.addEventListener("change", (event) => {
            if (event.target.matches("#horizontal")) {

                const horizontalToggle = event.target
                const toggle = horizontalToggle.checked;
                const date = document.querySelector("#datepicker").value;
                console.log('toggle value:', toggle); 

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
            button.addEventListener('click', (event) => {
                var bookingFormUrl = event.target.getAttribute('data-booking-form-url');
                
                fetch(bookingFormUrl)
                    .then(response => response.text())
                    .then(html => {
                        var formContainer = event.target.closest('.day-section').querySelector('.form-container');
                        formContainer.style.maxHeight = "0";
                        formContainer.style.opacity = "0";
                        formContainer.innerHTML = html;
        
                        setTimeout(() => {
                            formContainer.style.maxHeight = "500px";
                            formContainer.style.opacity = "1";
                        }, 100);
        
                        // This needs to be fixed to work also on fullday view
                        var sectionDate = event.target.closest('.day-section').querySelector('.section-date').dataset.date;
                        var checkInInput = formContainer.querySelector('#arrival-date');
                        checkInInput.value = sectionDate;
        
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
                    })
                    .catch(error => {
                        console.warn(error);
                    });
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
            button.addEventListener('click', (event) => {
                // var newcleanFormUrl = event.target.getAttribute('data-newclean-form-url');
                var newcleanFormUrl = "/minilogistic/newcleanform/";

                
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
                        var dateValue = new Date(sectionDate);

                        // Set the value of the clean date input field with the extracted date value
                        var cleanDateInput = formContainer.querySelector('#clean-date');
                        cleanDateInput.value = sectionDate;

                        // Make form disappear when .cancel-form is clicked
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

                        
                    })
                    .catch(error => {
                        console.warn(error);
                    });
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

        document.body.addEventListener("submit", (event) => {

            event.preventDefault();
            event.stopImmediatePropagation();
           
            const form = event.target;

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

            if (form.matches("#booking-form")) {
                const formData = new FormData(form);

                
        
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

        
            if (form.matches("#newclean-form")) {

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

                //console.log(formData)
        
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
                                console.log("FulldatePicker condition triggered")
                                // Refresh the front-end view 
                                updateFullday(date)
                            }
                        } else {
                            throw new Error("Error adding clean.");
                        }
                    })
                    .catch((error) => console.error(error));
            }            
        });


        // ----------------------------------------------- //
        // --------------- ADD COMMENT ------------------- //

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
                        div.className = newComment.fields.clean_belong ? `clean-comment-container comment-color-${newComment.fields.color}` : `booking-comment-container comment-color-${newComment.fields.color}`;

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
    
    } 

// ----------------------------------------------------------------------------------------- //
// ----------------------------------------------------------------------------------------- //



    // Add arrival time field to new clean form when same day is selected
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


    createEventListeners();

});
  
  
