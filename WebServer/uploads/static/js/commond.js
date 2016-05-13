/**
 * Created by virgil on 16/5/7.
 */

function showAlert(string){
        tip = $('#alert_tip');
        tip.html(string);
        tip.show();
        setTimeout('tip.fadeOut("slow")',2000);
}

function alertWithTitleAndBody(title,body){
    $('#alertModelTitle').text(title);
    $('#alertModelBody').text(body);
    var model = $('#alertModel');
     model.modal('show');
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}