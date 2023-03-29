document.addEventListener("DOMContentLoaded", () => {
    const datePicker = document.querySelector("#datepicker");
    const selectedDate = document.querySelector("#selected-date");
    const daySectionContainer = document.querySelector(".day-section-container");
  
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


    // Define function to create event listeners for Add buttons to open forms
    function createEventListeners() {

        // Booking Form //
        
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
                        var sectionDate = event.target.closest('.day-section').querySelector('.section-date').textContent;
                        var dateValue = new Date(sectionDate);

                        // Set the value of the check-in input field with the extracted date value
                        var checkInInput = formContainer.querySelector('#check-in');
                        checkInInput.valueAsDate = dateValue;
                    })
                    .catch(error => {
                        console.warn(error);
                    });
            });
        });

        // Hide Add Clean and Add Booking buttons when booking form is opened //

        const bookingButtons = document.querySelectorAll('.booking-button');
        const cleanButtons = document.querySelectorAll('.clean-button');
        const forms = document.querySelectorAll('.form-container');
        
        bookingButtons.forEach((button) => {
            button.addEventListener('click', function (event) {
            const formContainer = event.target.closest('.day-section').querySelector('.form-container');
            formContainer.style.opacity = 1;
        
            cleanButtons.forEach((btn) => (btn.style.opacity = 0));
            bookingButtons.forEach((btn) => (btn.style.opacity = 0));
        
            const checkInDate = event.target.closest('.day-section').querySelector('.section-date').textContent;
            formContainer.querySelector('#check-in').value = formatDate(checkInDate);
            });
        });
        
        forms.forEach((form) => {
            form.addEventListener('submit', function (event) {
            event.preventDefault();
        
            // Display Add Clean and Add Booking buttons again when form is submitted
            cleanButtons.forEach((btn) => (btn.style.opacity = 1));
            bookingButtons.forEach((btn) => (btn.style.opacity = 1));
        
            form.style.opacity = 0;
            form.style.maxHeight = "0"; // Shrink day-section back to size
            });
        });


        // New Clean Form // Note: I can probably make Booking Form and New Clean Form sections from the same code.. Alot of repetition here...

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
                        var sectionDate = event.target.closest('.day-section').querySelector('.section-date').textContent;
                        var dateValue = new Date(sectionDate);

                        // Set the value of the clean date input field with the extracted date value
                        var cleanDateInput = formContainer.querySelector('#clean-date');
                        cleanDateInput.valueAsDate = dateValue;
                    })
                    .catch(error => {
                        console.warn(error);
                    });
            });
        });

        // Hide Add Clean and Add Booking buttons when new clean form is opened //
        cleanButtons.forEach((button) => {
            button.addEventListener('click', function (event) {
            const formContainer = event.target.closest('.day-section').querySelector('.form-container');
            formContainer.style.opacity = 1;
        
            cleanButtons.forEach((btn) => (btn.style.opacity = 0));
            bookingButtons.forEach((btn) => (btn.style.opacity = 0));
        
            const cleanDate = event.target.closest('.day-section').querySelector('.section-date').textContent;
            formContainer.querySelector('#clean-date').value = formatDate(cleanDate);
            });
        });
        
        forms.forEach((form) => {
            form.addEventListener('submit', function (event) {
            event.preventDefault();
            // Display Add Clean and Add Booking buttons when form is submitted
            cleanButtons.forEach((btn) => (btn.style.opacity = 1));
            bookingButtons.forEach((btn) => (btn.style.opacity = 1));
        
            form.style.opacity = 0;
            form.style.maxHeight = "0"; // Shrink back to original size
            });
        });

    } 
    
    createEventListeners();

});
  
  
