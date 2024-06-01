document.getElementById('editPersonalInfoForm').addEventListener('submit', function(event) {
    event.preventDefault();
    // Add any custom form validation here if needed
    
    // Submit the form using fetch or XMLHttpRequest for AJAX submission
    // or simply call form.submit() for a standard form submission
    this.submit();
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