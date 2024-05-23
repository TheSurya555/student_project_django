  document.addEventListener('DOMContentLoaded', function() {
    function showSection(sectionId, linkId) {
      const sections = document.querySelectorAll('.content-section');
      const links = document.querySelectorAll('.sidebar a');
      
      sections.forEach(section => section.classList.remove('active'));
      links.forEach(link => link.classList.remove('active'));
      
      document.getElementById(sectionId).classList.add('active');
      document.getElementById(linkId).classList.add('active');
    }

    document.getElementById('myInfoLink').addEventListener('click', function(event) {
      event.preventDefault();
      showSection('myInfoSection', 'myInfoLink');
    });

    document.getElementById('projectsLink').addEventListener('click', function(event) {
      event.preventDefault();
      showSection('projectsSection', 'projectsLink');
    });

    document.getElementById('billingLink').addEventListener('click', function(event) {
      event.preventDefault();
      showSection('billingSection', 'billingLink');
    });

    document.getElementById('projectcompleteLink').addEventListener('click', function(event) {
      event.preventDefault();
      showSection('projectcompleteSection', 'projectcompleteLink');
    });

    document.getElementById('testLink').addEventListener('click', function(event) {
      event.preventDefault();
      showSection('testSection', 'testLink');
    });

    document.getElementById('connectLink').addEventListener('click', function(event) {
      event.preventDefault();
      showSection('connectSection', 'connectLink');
    });
  });  

  document.getElementById('uploadButton').addEventListener('click', function() {
    document.getElementById('fileInput').click();
  });

  document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
      console.log('File selected:', file.name);
      // You can add further processing here, like uploading the file
    }
  });  

  document.getElementById('socialMediaForm').addEventListener('submit', function(event) {
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
  


  

// JavaScript for handling "Start Test" and "Submit Link" functionality

document.getElementById('startTestButton').addEventListener('click', function() {
  alert('Test started! Follow the instructions to complete your test.');
  // Additional functionality to start the test can be added here
});



document.getElementById('completedProjectForm').addEventListener('submit', function(event) {
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

document.getElementById('submitAnswerLinkButton').addEventListener('click', function() {
  const answerLink = document.getElementById('answerLink').value;
  if (answerLink) {
    alert('Your answer link has been submitted: ' + answerLink);
    // Additional functionality to handle the link submission can be added here
  } else {
    alert('Please enter a valid link.');
  }
});
