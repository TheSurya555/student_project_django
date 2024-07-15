document.addEventListener('DOMContentLoaded', function() {

  // Function to show active section and highlight link
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

  // Array of links and sections
  const links = [
      { linkId: 'myInfoLink', sectionId: 'myInfoSection' },
      { linkId: 'projectsLink', sectionId: 'projectsSection' },
      { linkId: 'billingLink', sectionId: 'billingSection' },
      { linkId: 'projectcompleteLink', sectionId: 'projectcompleteSection' },
      { linkId: 'testLink', sectionId: 'testSection' },
      { linkId: 'connectLink', sectionId: 'connectSection' }
  ];

  // Add event listeners for each link
  links.forEach(({ linkId, sectionId }) => {
      const link = document.getElementById(linkId);
      if (link) {
          link.addEventListener('click', function(event) {
              event.preventDefault();
              showSection(sectionId, linkId);
          });
      }
  });

  // Handle resume display in modal
  const resumeModal = document.getElementById('resumeModal');
  const resumeEmbed = document.getElementById('resumeEmbed');

  if (resumeModal && resumeEmbed) {
      resumeModal.addEventListener('show.bs.modal', function(event) {
          // Load resume into the embed element
          if (resumeEmbed && resumeEmbed.src === '') {
              const resumeUrl = resumeEmbed.dataset.resumeUrl;
              if (resumeUrl) {
                  resumeEmbed.src = resumeUrl;
              } else {
                  resumeEmbed.parentElement.innerHTML = '<p>No resume uploaded.</p>';
              }
          }
      });

      resumeModal.addEventListener('hidden.bs.modal', function(event) {
          // Clear the resume embed when modal is closed
          resumeEmbed.src = '';
      });
  }

  // Handle file upload button
  const uploadButton = document.getElementById('uploadButton');
  const fileInput = document.getElementById('fileInput');

  if (uploadButton && fileInput) {
      uploadButton.addEventListener('click', function() {
          fileInput.click();
      });
  }

  // Handle social media form submission
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

  // Handle completed project form submission
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
          // Show the success message or handle further actions
      });
  }

  // Handle answer link submission
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
          // Show the success message or handle further actions
      });
  }
});
