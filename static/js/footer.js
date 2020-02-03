const langSelect = document.getElementById("js-lang");

const handleLangChange = () => {
    const selected = langSelect.value;


    const newURL = `${window.location.protocol}//${window.location.host}/users/switch-language?lang=${selected}`

    fetch(newURL).then(() => window.location.reload());
}


langSelect.addEventListener("change", handleLangChange);

