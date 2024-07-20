document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('form').addEventListener('submit', (event) => {
    event.preventDefault();
    fetch('emails',{
      method:'POST',
      body:JSON.stringify({
        recipients:document.querySelector('#compose-recipients').value,
        subject:document.querySelector('#compose-subject').value,
        body:document.querySelector('#compose-body').value
      })
    })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent');
  })
  .catche(error =>{
    console.log("Error:",error)
  })
  
  });
  // By default, load the inbox
  load_mailbox('inbox');
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

  // To show emails
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      console.log(emails);

      const emailContainer = document.createElement('div');

      emails.forEach(email => {
        const emailDiv = document.createElement('div');
        emailDiv.classList.add('email');
        emailDiv.dataset.id = email.id;
        emailDiv.innerHTML = `
          <span class="sender">${email.sender}</span>
          <span class="subject">${email.subject}</span>
          <span class="timestamp">${email.timestamp}</span>
        `;
        if (email.read) {
          emailDiv.classList.add('read');
        }
        emailContainer.append(emailDiv);
      });

      document.querySelector('#emails-view').append(emailContainer);

      // To update email status
      if(mailbox != 'inbox'){
        document.querySelectorAll('.email').forEach(email => {
          email.classList.add('read');
        });
      }
      document.querySelectorAll('.email').forEach(email => {
        if (mailbox === 'inbox') {
          console.log('time to add event listener');
          email.addEventListener('click', () => {
            console.log(`Email ID: ${email.dataset.id} clicked`); // Log the email ID
            fetch(`/emailStatus/${email.dataset.id}`, { // Ensure the URL is correct
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json'
              }
            })
            .then(response => response.json())
            .then(result => {
              console.log(result);
              if (result.message) {
                // Update the email element's class to reflect the read status
                email.classList.add('read');
              } else {
                console.log("Error:", result.error);
              }
            })
            .catch(error => {
              console.log("Error:", error);
            });
          });
        }
      });
    })
    .catch(error => {
      console.log("Error:", error);
    });
}