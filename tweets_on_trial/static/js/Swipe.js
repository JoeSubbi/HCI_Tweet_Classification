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

            inputJudgement = 1;

            confirmBool = this.confirm("You have selected negative, offensive, confirm or redo?")

            checkRespnse(confirmBool);

            map[37] = false;

                //up arrow
        } else if (map[38] && isNegative) {

            confirmBool = this.confirm("You have selected negative, both offensive and agrressive, confirm or redo?")

            checkRespnse(confirmBool);

            map[38] = false;

            //right arrow
        } else if (map[39] && isNegative) {

            confirmBool = this.confirm("You have selected negative, aggressive, confirm or redo?")

            checkRespnse(confirmBool);
            map[39] = false;

            //down arrow
        } else if (map[40] && isNegative) {

            confirmBool = this.confirm("You have selected negative, neither aggressive nor offensive, confirm or redo?")

            checkRespnse(confirmBool);

            map[40] = false;

            //left arrow
        } else if (map[37]) {

            confirmBool = this.confirm("You have selected positive, confirm or redo?")

            checkRespnse(confirmBool);

            map[40] = false;
            //up arrow
        } else if (map[38]) {


            confirmBool = this.confirm("You have selected neutral, confirm or redo?")

            checkRespnse(confirmBool);

            map[38] = false;

            //right arrow
        } else if (map[39]) {

           

            map[39] = false;

            //down arrow
        } else if (map[40]) {

            confirmBool = this.confirm("You have selected skip, confirm or redo?")

            checkRespnse(confirmBool);

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




}

function sendData() {

    $.ajax({
        type: 'POST',
        data: {
            'input': inputJudgement,
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