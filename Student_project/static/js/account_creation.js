document.addEventListener("DOMContentLoaded", function() {
    const sections = {
        profileSectionLink: document.getElementById("profileSection"),
        educationSectionLink: document.getElementById("educationSection"),
        projectExperienceSectionLink: document.getElementById("projectExperienceSection")
    };

    // Iterate through the section links and add event listeners if they exist
    Object.keys(sections).forEach(linkId => {
        const linkElement = document.getElementById(linkId);
        if (linkElement && sections[linkId]) {
            linkElement.addEventListener("click", function(event) {
                event.preventDefault();
                showSection(sections[linkId]);
            });
        }
    });

    function showSection(section) {
        Object.values(sections).forEach(sec => {
            if (sec) {
                sec.classList.remove("active");
            }
        });
        if (section) {
            section.classList.add("active");
        }

        // Remove active class from all links and add it to the corresponding link
        document.querySelectorAll('.sidebar a').forEach(link => link.classList.remove('active'));
        const activeLink = document.getElementById(`${section.id}Link`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }

    // Function to handle showing the next section
    window.showNextSection = function(nextSectionId) {
        const nextSection = document.getElementById(nextSectionId);
        if (nextSection) {
            showSection(nextSection);
        }
    };

    // Handle form submissions
    const forms = ["profileDetailsForm", "educationForm", "projectExperienceForm"];

    forms.forEach(formId => {
        const formElement = document.getElementById(formId);
        if (formElement) {
            formElement.addEventListener("submit", function(event) {
                event.preventDefault(); // Prevent the default form submission

                // Prepare form data for submission
                const formData = new FormData(this);

                // Submit the form data using fetch
                fetch("/submit-form", {
                    method: "POST",
                    body: formData
                })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error("Network response was not ok.");
                    }
                })
                .then(data => {
                    if (data.success) {
                        alert("Form submitted successfully!");
                        this.reset();
                    } else {
                        alert("Error: " + data.message);
                    }
                })
                .catch(error => {
                    console.error("There was a problem with the fetch operation:", error);
                    alert("An error occurred while submitting the form. Please try again.");
                });
            });
        }
    });
});
