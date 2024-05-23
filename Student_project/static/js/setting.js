$(document).ready(function() {
  $('#editPersonalInfoForm').on('submit', function(event) {
    event.preventDefault();
    
    // Get the updated values from the form
    var updatedName = $('#editName').val();
    var updatedEmail = $('#editEmail').val();
    var updatedPhone = $('#editPhone').val();

    // Update the profile details on the page
    $('#profileName').text(updatedName);
    $('#profileEmail').text(updatedEmail);
    $('#profilePhone').text(updatedPhone);

    // Close the modal
    $('#editPersonalInfoModal').modal('hide');
  });
});  
  
  
  $(document).ready(function() {
    $('.sidebar a').click(function(e) {
      e.preventDefault();
      $('.sidebar a').removeClass('active');
      $(this).addClass('active');
      $('.content-section').removeClass('active');
      $('#' + $(this).attr('id').replace('Link', 'Section')).addClass('active');
    });

    $('#themeToggle').change(function() {
      if ($(this).val() == 'Dark Mode') {
        $('body').addClass('dark-mode');
      } else {
        $('body').removeClass('dark-mode');
      }
    });

    $('#changePasswordForm').on('submit', function(e) {
      e.preventDefault();
      let newPassword = $('#newPassword').val();
      let confirmPassword = $('#confirmPassword').val();

      if (newPassword !== confirmPassword) {
        $('#confirmPassword').addClass('is-invalid');
      } else {
        $('#confirmPassword').removeClass('is-invalid');
        // Submit form via AJAX or other methods
        alert('Password changed successfully');
        $('#changePasswordModal').modal('hide');
      }
    });
  });