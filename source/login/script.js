document.getElementById('loginForm').onsubmit = async function (event) {
    event.preventDefault();

    const user = document.getElementById('user').value;
    const pass = document.getElementById('pass').value;
    const form = document.getElementById('loginForm');
    const level = form.getAttribute("data-level");

    // Enviar solicitud al servidor con fetch
    const response = await fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: user,
            password: pass,
            level: level
        })
    });

    const result = await response.json();
    const errorMsg = document.getElementById("error");
    if (result.status === "success") {
        errorMsg.textContent = result.message;
        errorMsg.classList.remove("error");
        errorMsg.classList.add("success");

        // Redirigir al siguiente nivel, si hay más niveles
        const currentLevelNumber = parseInt(level.replace("level", ""));
        if (currentLevelNumber < 5) {
            setTimeout(() => {
                window.location.href = `level${currentLevelNumber + 1}.html`;
            }, 2000);
        } else {
            errorMsg.textContent += " ¡Has completado todos los niveles!";
        }
    } else {
        errorMsg.textContent = result.message;
        errorMsg.classList.remove("success");
        errorMsg.classList.add("error");
    }
};
