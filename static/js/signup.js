const emailInput = document.getElementById('emailInput');


function focusEmailInput() {
    if (emailInput.classList.contains("has_error")) {
        emailInput.classList.remove("has_error")
    }
    const parent = emailInput.parentNode.parentNode;
    if (parent.classList.contains("has_error")) {
        parent.classList.remove("has_error")
    }
};

emailInput.addEventListener("focus", () => focusEmailInput());
