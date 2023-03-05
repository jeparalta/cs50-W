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

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // TODO Display emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    //const sender = emails[0].sender;
    //console.log(sender);
    
   /* for (let i = 0; i < emails.length; i++) {
      console.log(emails[i].sender);
      let div = document.createElement('div');
      div.className = 'email-item'
      div.innerHTML = emails[i].sender + emails[i].subject + emails[i].timestamp;
      document.querySelector('#emails-view').append(div);
    }*/
    const emailsView = document.querySelector('#emails-view');
    emails.forEach(email => {
    console.log(email.sender);
    let div = document.createElement('div');
    div.className = 'email-item';
    div.innerHTML = 
    `<div class="email-details">
        <span class="email-sender">${email.sender}</span>
        <span class="email-subject">${email.subject}</span>
    </div>
    <div class="email-timestamp">${email.timestamp}</div>`;
    emailsView.append(div);
}); 

  });

  

}


// TODO 

// Send email
function send_email() {
  console.log('Test code')
  
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

