function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


  
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

//Global variables for determining what is being added to db
var isNegative = false;
var inputJudgement;

$(document).ready(function () {

    var map = {};
    var confirmBool = false;
    onkeydown = onkeyup = function (e) {
        e = e || event; // to deal with IE
        map[e.keyCode] = e.type == 'keydown';
        //Left arrow
        if (map[37] && isNegative) {

            map[37] = false;

            inputJudgement = 1;

            confirmBool = this.confirm("You have selected negative, offensive, confirm or redo?")

            checkRespnse(confirmBool);

            map[37] = false;

                //up arrow
        } else if (map[38] && isNegative) {

            map[38] = false;

            inputJudgement = 2;

            confirmBool = this.confirm("You have selected negative, both offensive and agrressive, confirm or redo?")

            checkRespnse(confirmBool);

            map[38] = false;

            //right arrow
        } else if (map[39] && isNegative) {

            map[39] = false;

            inputJudgement = 3;

            confirmBool = this.confirm("You have selected negative, aggressive, confirm or redo?")

            checkRespnse(confirmBool);
            map[39] = false;

            //down arrow
        } else if (map[40] && isNegative) {

            map[40] = false;

            resetJudgement();

            map[40] = false;

            //left arrow
        } else if (map[37]) {

            map[37] = false;

            inputJudgement = 1;

            confirmBool = this.confirm("You have selected positive, confirm or redo?")

            checkRespnse(confirmBool);

            map[37] = false;
            //up arrow
        } else if (map[38]) {

            map[38] = false;

            inputJudgement = 2;

            confirmBool = this.confirm("You have selected neutral, confirm or redo?")

            checkRespnse(confirmBool);

            map[38] = false;

            //right arrow
        } else if (map[39]) {

            map[39] = false;

            
            document.getElementById("left").innerHTML = "Offensive";
            document.getElementById("right").innerHTML = "Agressive";
            document.getElementById("up").innerHTML = "Both";
            document.getElementById("down").innerHTML = "Back";
            isNegative = true;

            map[39] = false;

            //down arrow
        } else if (map[40]) {

            map[40] = false;

            inputJudgement = 0;

            confirmBool = this.confirm("You have selected skip, are you sure?")

            if (responseBool) {

                this.location.reload();
        
            } else {
        
                resetJudgement();
        
            };

            map[40] = false;

        };

    };

});

function checkRespnse(responseBool) {


    if (responseBool) {

        sendData();

    } else {

        resetJudgement();

    };

}

function resetJudgement() {

    document.getElementById("left").innerHTML = "Positive";
    document.getElementById("right").innerHTML = "Negative";
    document.getElementById("up").innerHTML = "Neutral";
    document.getElementById("down").innerHTML = "Skip";
    isNegative = flase;

}

function sendData() {

    console.info("test")

    $.ajax({
        type: 'POST',
        data: {
            'inputJudgement': inputJudgement,
            'isNegative': isNegative,
        },

        success: function (response) {

            console.info("success")

        },

        error: function () {

            console.info("failure")

        }

    });

};