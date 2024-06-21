document.addEventListener('DOMContentLoaded', function() {
  function showSection(sectionId, linkId) {
      const sections = document.querySelectorAll('.content-section');
      const links = document.querySelectorAll('.sidebar a');
      
      sections.forEach(section => section.classList.remove('active'));
      links.forEach(link => link.classList.remove('active'));
      
      const section = document.getElementById(sectionId);
      const link = document.getElementById(linkId);
      
      if (section && link) {
          section.classList.add('active');
          link.classList.add('active');
      }
  }

  const links = [
      { linkId: 'myInfoLink', sectionId: 'myInfoSection' },
      { linkId: 'projectsLink', sectionId: 'projectsSection' },
      { linkId: 'billingLink', sectionId: 'billingSection' },
      { linkId: 'projectcompleteLink', sectionId: 'projectcompleteSection' },
      { linkId: 'testLink', sectionId: 'testSection' },
      { linkId: 'connectLink', sectionId: 'connectSection' }
  ];

  links.forEach(({ linkId, sectionId }) => {
      const link = document.getElementById(linkId);
      if (link) {
          link.addEventListener('click', function(event) {
              event.preventDefault();
              showSection(sectionId, linkId);
          });
      }
  });

  const uploadButton = document.getElementById('uploadButton');
  const fileInput = document.getElementById('fileInput');

  if (uploadButton && fileInput) {
      uploadButton.addEventListener('click', function() {
          fileInput.click();
      });

      fileInput.addEventListener('change', function(event) {
          const file = event.target.files[0];
          if (file) {
              console.log('File selected:', file.name);
              // You can add further processing here, like uploading the file
          }
      });
  }

  const socialMediaForm = document.getElementById('socialMediaForm');

  if (socialMediaForm) {
      socialMediaForm.addEventListener('submit', function(event) {
          event.preventDefault();
          
          const platform = document.getElementById('socialMediaPlatform').value;
          const link = document.getElementById('socialMediaLink').value;
          
          if (link) {
              const container = document.getElementById('socialMediaLinksContainer');
              const existingLinks = container.querySelectorAll('p strong');
              let duplicateFound = false;
      
              existingLinks.forEach(function(existingLink) {
                  if (existingLink.textContent.includes(platform)) {
                      duplicateFound = true;
                  }
              });
      
              if (duplicateFound) {
                  alert(`You have already added a link for ${platform}.`);
              } else {
                  // Hide the no links message
                  document.getElementById('noLinksMessage').style.display = 'none';
                  
                  // Create a new link element
                  const newLink = document.createElement('div');
                  newLink.className = 'mb-2';
                  newLink.innerHTML = `
                      <p><strong>${platform}:</strong> <a href="${link}" target="_blank">${link}</a></p>
                  `;
                  
                  // Append the new link to the container
                  container.appendChild(newLink);
                  
                  // Close the modal after submission
                  $('#socialMediaModal').modal('hide');
                  
                  // Optionally, clear the form fields
                  document.getElementById('socialMediaPlatform').selectedIndex = 0;
                  document.getElementById('socialMediaLink').value = '';
              }
          }
      });
  }

  const completedProjectForm = document.getElementById('completedProjectForm');

  if (completedProjectForm) {
      completedProjectForm.addEventListener('submit', function(event) {
          event.preventDefault(); // Prevent the form from submitting the traditional way
          const projectLink = document.getElementById('projectLink').value;
          if (projectLink) {
              alert('Your project complete link has been submitted: ' + projectLink);
              // Additional functionality to handle the link submission can be added here
          } else {
              alert('Please enter a valid link.');
          }
          // Show the success message
      });
  }

  const submitAnswerLinkButton = document.getElementById('submitAnswerLinkButton');

  if (submitAnswerLinkButton) {
      submitAnswerLinkButton.addEventListener('click', function() {
          const answerLink = document.getElementById('answerLink').value;
          if (answerLink) {
              alert('Your answer link has been submitted: ' + answerLink);
              // Additional functionality to handle the link submission can be added here
          } else {
              alert('Please enter a valid link.');
          }
      });
  }
});
