document.addEventListener("DOMContentLoaded", () => {

    const mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };

    document.addEventListener("mousemove", (e) => {
        mouse.x = e.pageX;
        mouse.y = e.pageY;
        createParticle(mouse.x, mouse.y);
    });

    function createParticle(x, y) {

        const particle = document.createElement("div");
        particle.className = "dream-particle";

        const size = Math.random() * 16 + 8;
        particle.style.width = size + "px";
        particle.style.height = size + "px";

        particle.style.left = x + "px";
        particle.style.top = y + "px";

        const colors = [
            "rgba(255,200,255,0.9)",
            "rgba(230,180,255,0.8)",
            "rgba(210,160,255,0.8)",
            "rgba(255,190,230,0.8)"
        ];

        const color = colors[Math.floor(Math.random() * colors.length)];

        particle.style.background = `radial-gradient(circle,
            ${color} 0%,
            ${color.replace("0.9","0.5")} 40%,
            transparent 80%)`;

        document.body.appendChild(particle);

        const angle = Math.random() * Math.PI * 2;
        const distance = Math.random() * 40;

        const xMove = Math.cos(angle) * distance;
        const yMove = Math.sin(angle) * distance;

        particle.animate([
            {
                transform: "translate(-50%, -50%) scale(1)",
                opacity: 1
            },
            {
                transform: `translate(${xMove}px, ${yMove}px) scale(0.3)`,
                opacity: 0
            }
        ], {
            duration: 900,
            easing: "ease-out"
        });

        setTimeout(() => {
            particle.remove();
        }, 900);
    }

});
