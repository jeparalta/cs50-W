document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');

  // Send email when form submitted
  document.querySelector('#compose-form').onsubmit = () => {
  send_email();
  load_mailbox('sent');
  return false;
  };


});



function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}



function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // TODO Display emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails for testing
    //console.log(emails);
  
    emails.forEach(email => {

        // Create new div, add classname and id
        let div = document.createElement('div');
        div.className = 'email-item';
        div.dataset.id = `${email.id}`
        
        // Add email details to div
        div.innerHTML = `
        <div class="email-details">
          <span class="email-sender">${email.sender}</span>
          <span class="email-subject">${email.subject}</span>
        </div>
        <div class="email-timestamp">${email.timestamp}</div>`;

        // Append to Email view section
        document.querySelector('#emails-view').append(div);

        // If email has been read make grey
        if (email.read === true) {
          div.style.backgroundColor = "lightgrey"; 
        };

        // Add click event listener for email item
        div.addEventListener('click', () => {
          email_view(email.id);
        });
    }); 

  });

}



function email_view(email_id) {
  
  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Load email content in html
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      



      document.querySelector('#email-view').innerHTML = ` 
      <div class="email-header">
    <div><b>From:</b> ${email.sender}</div>
    <div class="email-timestamp">${email.timestamp}</div>
    </div>
    <div class="email-recipient"><b>To:</b> ${email.recipients}</div>
    <div><b>Subject:</b> ${email.subject}</div>
    <div class="email-body">${email.body}</div>`

    // Archive/Unarchive email
    const user = document.querySelector('h2').innerHTML
    if (email.sender !== user) {
      if (email.archived === false) {
        console.log('Archived')
        let archiveButton = document.createElement('button');
        archiveButton.innerHTML = 'Archive';
        archiveButton.className= "btn btn-sm btn-outline-secondary"
        document.querySelector('#email-view').append(archiveButton);

        archiveButton.addEventListener('click', () => {
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: true
            })
          })
          load_mailbox('inbox');
        });
        

      }
      else {
        console.log('Not Archived')
        let unarchiveButton = document.createElement('button');
        unarchiveButton.innerHTML = 'Unarchive'
        unarchiveButton.className= "btn btn-sm btn-outline-secondary"
        document.querySelector('#email-view').append(unarchiveButton);

        unarchiveButton.addEventListener('click', () => {
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: false
            })
          })
          load_mailbox('inbox');
        });
        
      }
    }
  });

  // Mark email as read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  


}

// Send email
function send_email() {
  
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
  

}

