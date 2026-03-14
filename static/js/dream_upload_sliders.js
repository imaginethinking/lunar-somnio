function attachSlider(sliderId, valueId) {
    const slider = document.getElementById(sliderId);
    const value = document.getElementById(valueId);

    if (!slider || !value) return;

    value.textContent = slider.value;

    slider.addEventListener("input", function () {
        value.textContent = this.value;
    });
}

document.addEventListener("DOMContentLoaded", function () {

    attachSlider("id_sleep_quality", "sleep_value");
    attachSlider("id_lucidity", "lucidity_value");

});

