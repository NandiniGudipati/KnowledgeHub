
function showLogin() {
    alert("Login functionality is coming soon!");
}

function showRegister() {
    alert("Employee registration is coming soon!");
}

function searchKnowledge() {

    const searchValue = document
        .getElementById("searchInput")
        .value
        .trim();

    if (searchValue === "") {
        alert("Please enter something to search.");
        return;
    }

    alert("You searched for: " + searchValue);
}
