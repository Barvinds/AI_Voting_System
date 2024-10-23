 // Get a reference to the logout button by its class name
const logoutButton = document.querySelector('.logout-button');

// Add a click event listener to the logout button
logoutButton.addEventListener('click', function () {
    // Redirect to the login page
    window.location.href = 'Login.html';
});


function updateTime() {
            const currentTimeElement = document.getElementById("time");
            const now = new Date();
            const hours = now.getHours().toString().padStart(2, "0");
            const minutes = now.getMinutes().toString().padStart(2, "0");
            const seconds = now.getSeconds().toString().padStart(2, "0");
            const timeString = `${hours}:${minutes}:${seconds}`;
            currentTimeElement.textContent = timeString;
        }

        // Update the time every second
        setInterval(updateTime, 1000);

        // Initial time update
        updateTime();

        document.addEventListener('DOMContentLoaded', function () {
            var voteButton = document.getElementById('vote_button');
            var partiesButton = document.getElementById('parties_button');
            var aboutButton = document.getElementById('about_button');
          
            voteButton.addEventListener('click', function () {
              // Redirect to qr-code.html when Vote button is clicked
              window.location.href = 'face_verification.html';
            });
          
            partiesButton.addEventListener('click', function () {
              // Redirect to parties.html when Parties button is clicked
              window.location.href = 'parties_view.html';
            });

            aboutButton.addEventListener('click', function () {
              // Redirect to parties.html when Parties button is clicked
              window.location.href = 'https://www.eci.gov.in/about-eci';
            });
          });
          


  