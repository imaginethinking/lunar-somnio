document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".dream-card-particles");

    cards.forEach((card) => {
        let lastParticleTime = 0;

        card.addEventListener("mousemove", (e) => {
            const now = Date.now();
            if (now - lastParticleTime < 45) return;
            lastParticleTime = now;

            const x = e.clientX;
            const y = e.clientY;
            const baseColor = card.dataset.dreamColour || "#ffffff";

            createStarParticle(x, y, baseColor);
        });
    });

    function hexToRgba(hex, alpha) {
        if (!hex) return `rgba(255,255,255,${alpha})`;

        let cleanHex = hex.replace("#", "");

        if (cleanHex.length === 3) {
            cleanHex = cleanHex.split("").map((c) => c + c).join("");
        }

        const r = parseInt(cleanHex.substring(0, 2), 16);
        const g = parseInt(cleanHex.substring(2, 4), 16);
        const b = parseInt(cleanHex.substring(4, 6), 16);

        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    function createStarParticle(x, y, baseColor) {
        const star = document.createElement("div");
        star.className = "dream-star-particle";

        const size = Math.random() * 6 + 4; // 4px to 10px
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.left = `${x}px`;
        star.style.top = `${y}px`;

        const bright = hexToRgba(baseColor, 1);
        const soft = hexToRgba(baseColor, 0.35);

        star.style.background = `radial-gradient(circle, ${bright} 0%, ${bright} 35%, ${soft} 60%, transparent 100%)`;

        document.body.appendChild(star);

        const angle = Math.random() * Math.PI * 2;
        const distance = Math.random() * 18 + 6;
        const xMove = Math.cos(angle) * distance;
        const yMove = Math.sin(angle) * distance;

        star.animate(
            [
                {
                    transform: "translate(-50%, -50%) scale(0.6) rotate(0deg)",
                    opacity: 0
                },
                {
                    transform: "translate(-50%, -50%) scale(1.2) rotate(45deg)",
                    opacity: 1,
                    offset: 0.35
                },
                {
                    transform: `translate(${xMove}px, ${yMove}px) scale(0.2) rotate(90deg)`,
                    opacity: 0
                }
            ],
            {
                duration: 550,
                easing: "ease-out"
            }
        );

        setTimeout(() => {
            star.remove();
        }, 550);
    }
});