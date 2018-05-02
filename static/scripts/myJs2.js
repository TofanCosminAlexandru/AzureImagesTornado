var ulrToSend;
var descriptionToSend;

$(document).ready(function () {
    $.ajax({
        url: '/records',
        data: $('form').serialize(),
        type: 'POST',
        success: function (response) {
            for (var i = 0; i < response.length; i+=2) {
                console.log(response[i], response[i + 1]);
                //$("#imagesTbody").append("<tr><td scope = \"col\">" + response[i] + "</td > <td scope=\"col\">" + response[i + 1] + "</td><td scope=\"col\"><button type=\"button\" class=\"send_email\" data-toggle=\"modal\" data-target=\"#exampleModal\">Send Email</button></td> </tr>");
                $("#imagesTbody").append("<tr><td scope = \"col\" onclick = \"imageModal(this)\">" + response[i] + "</td > <td scope=\"col\">" + response[i + 1] + "</td><td scope=\"col\"><button type=\"button\" class=\"send_email\" data-toggle=\"modal\" data-target=\"#exampleModal\" onclick=\"getParamToSend(this)\">Send Email</button></td> </tr>");
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
});


$(function () {
    $('#sendEmail').click(function (e) {
        //console.log($('#recipient-name').val());
        e.preventDefault();
        ulrToSend = ulrToSend.split("https://")[1].split("/").join("~").split("?").join("^");
        console.log(descriptionToSend)
        var param = "/sendemail/" + $('#recipient-name').val() + "/" + ulrToSend + "/" + descriptionToSend;
        $.ajax({
            url: param,
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});

function getParamToSend(button) {
    ulrToSend = button.parentElement.parentElement.firstChild.innerHTML;
    descriptionToSend = button.parentElement.parentElement.childNodes[2].innerHTML;
}

function imageModal(link) {
    var modal = document.getElementById('myModal');
    var modalImg = document.getElementById("img01");
    var imageModalCloseX = document.getElementById("closeImageModal");

    var url = link.innerHTML;
    modal.style.display = "block";
    modalImg.src = url;

    imageModalCloseX.onclick = function () {
        modal.style.display = "none";
    }
}