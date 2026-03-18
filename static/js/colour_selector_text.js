const colourSelect = document.getElementById("id_colour");

function updateColour() {
    colourSelect.style.color = colourSelect.value;
}

colourSelect.addEventListener("change", updateColour);
updateColour();