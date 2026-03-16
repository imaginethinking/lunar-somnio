document.querySelectorAll(".reaction-form").forEach(form => {
    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const button = form.querySelector("button");
        const countSpan = button.querySelector(".reaction-count");
        const emoji = button.dataset.emoji;

        const response = await fetch(form.action, {
            method: "POST",
            body: new FormData(form)
        });

        const data = await response.json();

        if (!data.success) return;

        countSpan.textContent = data.count;

        if (emoji === "heart") {
            button.className = data.reacted ? "btn btn-sm btn-danger" : "btn btn-sm btn-outline-danger";
        }
        if (emoji === "laugh") {
            button.className = data.reacted ? "btn btn-sm btn-warning" : "btn btn-sm btn-outline-warning";
        }
        if (emoji === "surprised") {
            button.className = data.reacted ? "btn btn-sm btn-secondary" : "btn btn-sm btn-outline-secondary";
        }
        if (emoji === "sad") {
            button.className = data.reacted ? "btn btn-sm btn-primary" : "btn btn-sm btn-outline-primary";
        }
        if (emoji === "fire") {
            button.className = data.reacted ? "btn btn-sm btn-dark" : "btn btn-sm btn-outline-dark";
        }
    });
});