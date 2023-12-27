
// Assume these flags indicate whether the user is registered as an artist or photographer
let isArtistRegistered = false;
let isPhotographerRegistered = false;


function toggleRoleDropdown() {
    document.getElementById("roleDropdown").classList.toggle("show");
}

function switchRole(role) {
    document.getElementById("selectedRoleLabel").textContent = "Selected Role: " + role;
    toggleRoleDropdown();

    // Perform logic to update the user's role on the server
    alert(`Role switched to ${role}`);

    // Show or hide the relevant artwork collections based on the selected role
    const artworkCollectionsArtist = document.getElementById("artworkCollectionsArtist");
    const artworkCollectionsPhotographer = document.getElementById("artworkCollectionsPhotographer");
    if (role === "Switch to Artist") {
        artworkCollectionsArtist.style.display = "block";
        artworkCollectionsPhotographer.style.display = "none";
    } else if (role === "Switch to Photographer") {
        artworkCollectionsArtist.style.display = "none";
        artworkCollectionsPhotographer.style.display = "block";
    } else {
        artworkCollectionsArtist.style.display = "none";
        artworkCollectionsPhotographer.style.display = "none";
    }
}

// Check if the user is registered as an artist and enable/disable the button accordingly
const switchToArtistButton = document.querySelector("#roleDropdown button:nth-child(1)");
switchToArtistButton.style.display = isArtistRegistered ? "inline-block" : "none";

// Check if the user is registered as a photographer and enable/disable the button accordingly
const switchToPhotographerButton = document.querySelector("#roleDropdown button:nth-child(2)");
switchToPhotographerButton.style.display = isPhotographerRegistered ? "inline-block" : "none";