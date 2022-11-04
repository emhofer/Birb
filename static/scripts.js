// Only run code if a certain element exists
// https://stackoverflow.com/questions/20065314/checking-if-a-button-exists
$(document).ready(function(){

    // Delete confirmation only shows after detele button is clicked
    if(document.getElementById('deleteButton')) {

        let deleteButton = document.getElementById("deleteButton");

        let deleteConfirmation = document.getElementById("deleteConfirmation");

        deleteButton.onclick = function () {

            currentDisplay = deleteConfirmation.style.display;

            if (deleteConfirmation.style.display == "") {
                deleteConfirmation.style.display = "block";
            }

            else {
                deleteConfirmation.style.display = "";
            }
        };
    }

    // Update feed continuously
    // https://www.codeproject.com/Questions/161828/Using-XMLHttpRequest-refresh-intervals
    if(document.getElementById('feedDiv')) {

        function updateFeed() {

            var ajax = new XMLHttpRequest();

            ajax.onreadystatechange = function () {
                if (ajax.readyState == 4 && ajax.status == 200) {
                    $('#feedDiv').html(ajax.responseText);
                }
            };

            ajax.open('GET', '/feed', true)
            ajax.send();
        };

        updateFeed();
        setInterval(updateFeed, 2000);
    }


    // Update likes continuously
    if(document.getElementById('likesDiv')) {

        function updateLikes() {

            var ajax = new XMLHttpRequest();

            ajax.onreadystatechange = function () {
                if (ajax.readyState == 4 && ajax.status == 200) {
                    $('#likesDiv').html(ajax.responseText);
                }
            };

            let username = document.getElementById('usernameTitle').innerHTML;

            ajax.open('GET', '/likes?username=' + username, true);
            ajax.send();
        };

        updateLikes();
        setInterval(updateLikes, 2000);
    }


    // Update chirps continuously
    if(document.getElementById('chirpsDiv')) {

        function updateChirps() {

            var ajax = new XMLHttpRequest();

            ajax.onreadystatechange = function () {
                if (ajax.readyState == 4 && ajax.status == 200) {
                    $('#chirpsDiv').html(ajax.responseText);
                }
            };

            let username = document.getElementById('usernameTitle').innerHTML;

            ajax.open('GET', '/chirps?username=' + username, true);
            ajax.send();
        };

        updateChirps();
        setInterval(updateChirps, 2000);
    }
});