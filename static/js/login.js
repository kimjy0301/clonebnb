const passwordInput = document.getElementById('passwordInput');
const emailInput = document.getElementById('emailInput');


function focusInput(el) {
    el.value = ""
    const parent = el.parentNode.parentNode;
    if (parent.classList.contains("has_error")) {
        parent.classList.remove("has_error")
    }
};

emailInput.addEventListener("focus", () => focusInput(emailInput));
passwordInput.addEventListener("focus", () => focusInput(passwordInput));