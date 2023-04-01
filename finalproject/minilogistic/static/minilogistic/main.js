document.addEventListener("DOMContentLoaded", () => {
    const datePicker = document.querySelector("#datepicker");
    const daySectionContainer = document.querySelector(".day-section-container");

    // ----------- DATEPICKER ---------------- //
    datePicker.addEventListener("input", () => {  

      const date = datePicker.value; // get new date selected on date picker
    
      //console.log(date);
  
      daySectionContainer.style.opacity = 0; //make old days go away smoothly using css transition
      fetch(`/minilogistic/days?selected=${date}`)
        .then((response) => response.json())
        .then((data) => {
          setTimeout(() => {
            daySectionContainer.innerHTML = data.rendered_day_section;
            daySectionContainer.style.opacity = 1; // make new days appear smoothly with css transition

            
            createEventListeners(); // Initialize event listeners for the new day-sections Add buttons to open forms

          }, 500); // Wait for 500ms before updating the content and making it visible again
        })
        .catch((error) => console.error(error));
    });

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

    


    // Define function to create event listeners for Add buttons to open forms
    function createEventListeners() {



        // ---------- Booking Form ------------- //


        // Display the form
        document.querySelectorAll('.booking-button').forEach((button) => {
            button.addEventListener('click', (event) => {
                var bookingFormUrl = event.target.getAttribute('data-booking-form-url');
                
                fetch(bookingFormUrl)
                    .then(response => response.text())
                    .then(html => {
                        // Find the .form-container element within the same day-section as the clicked button
                        var formContainer = event.target.closest('.day-section').querySelector('.form-container');
                        formContainer.style.maxHeight = "500px"; // Set max-height to 500px or a suitable value
                        // add the form
                        formContainer.innerHTML = html;

                        // Extract the date value from the .section-date element
                        var sectionDate = event.target.closest('.day-section').querySelector('.section-date').dataset.date;
                        var dateValue = new Date(sectionDate);

                        // Set the value of the check-in input field with the extracted date value
                        var checkInInput = formContainer.querySelector('#arrival-date');
                        checkInInput.value = sectionDate;
                    })
                    .catch(error => {
                        console.warn(error);
                    });
            });
        });

        // Hide (Add Clean) and (Add Booking) buttons when booking form is opened //

        const bookingButtons = document.querySelectorAll('.booking-button');
        const cleanButtons = document.querySelectorAll('.clean-button');
        const forms = document.querySelectorAll('.form-container');
        
        bookingButtons.forEach((button) => {
            button.addEventListener('click', function (event) {

            const formContainer = event.target.closest('.day-section').querySelector('.form-container');
            formContainer.style.opacity = 1;
        
            cleanButtons.forEach((btn) => (btn.style.opacity = 0));
            bookingButtons.forEach((btn) => (btn.style.opacity = 0));
        
            });
        });
        
       






        // -------- New Clean Form ---------- //                            Note: I can probably make Booking Form and New Clean Form sections from the same code.. Alot of repetition here...

        // Display form
        document.querySelectorAll('.clean-button').forEach((button) => {
            button.addEventListener('click', (event) => {
                var newcleanFormUrl = event.target.getAttribute('data-newclean-form-url');
                
                fetch(newcleanFormUrl)
                    .then(response => response.text())
                    .then(html => {
                        // Find the .form-container element within the same day-section as the clicked button
                        var formContainer = event.target.closest('.day-section').querySelector('.form-container');
                        // Make space for form
                        formContainer.style.maxHeight = "500px"; 
                        // Add the form
                        formContainer.innerHTML = html;
                        // Extract the date value from the .section-date element
                        var sectionDate = event.target.closest('.day-section').querySelector('.section-date').dataset.date;
                        var dateValue = new Date(sectionDate);

                        // Set the value of the clean date input field with the extracted date value
                        var cleanDateInput = formContainer.querySelector('#clean-date');
                        cleanDateInput.value = sectionDate;
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

        

        // When form is submitted
        document.body.addEventListener("submit", (event) => {
            event.preventDefault();
            event.stopImmediatePropagation();
            const form = event.target;

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
                            // Refresh the front-end view by triggering the date picker event
                            document.querySelector("#datepicker").dispatchEvent(new Event("input"));
                        } else {
                            throw new Error("Error adding booking.");
                        }
                    })
                    .catch((error) => console.error(error));
            }

        
            if (form.matches("#newclean-form")) {
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
                            // Refresh the front-end view by triggering the date picker event
                            document.querySelector("#datepicker").dispatchEvent(new Event("input"));
                        } else {
                            throw new Error("Error adding clean.");
                        }
                    })
                    .catch((error) => console.error(error));
            }

            
        });

        
    
        


    } 

   




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
  
  
