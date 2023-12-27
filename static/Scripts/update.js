function openBioEditor() {
    document.getElementById("bioEditor").style.display = "block";
}

function closeBioEditor() {
    document.getElementById("bioEditor").style.display = "none";
}

function updateBio() {
    // document.querySelector('#bioEditor textarea').value = document.getElementById("user-bio")
    const newBio = document.querySelector("#bioEditor textarea").value;
    if (newBio.trim() !== "") {
        document.getElementById("user-bio").textContent = newBio;
        closeBioEditor();
    } else {
        alert("Please enter a valid bio.");
    }
}