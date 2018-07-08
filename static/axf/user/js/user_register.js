function check_input() {
    var username_color = $("#username_info").css('color');
    
    console.log(username_color);
    
    if (username_color == "rgb(255, 0, 0)"){
        return false
    }
    var password = $("#exampleInputPassword").val();
    var password_confirm = $("#exampleInputPassword1").val();

    if (password.length>5){
        if (password === password_confirm){
            $("#exampleInputPassword").val(md5(password));
            return true
        }else {
            $("#repassword_info").html('两次输入密码不一致！').css('color', 'red');
            return false
        }
    }else{
        $("#password_info").html('密码长度不能少于5位').css('color', 'red');
        return false
    }

}

$(function () {
    $("#exampleInputUsername").change(function () {
        var username = $(this).val();
        console.log(username);
        $.getJSON("/axf/checkuser/", {"username": username}, function (data) {
        console.log(data);
        if (data.status == '200'){
            $("#username_info").html(data["msg"]).css('color', 'green')
        }else if (data.status == '901'){
            $("#username_info").html(data["msg"]).css('color', 'red')
        }
        })
    })
});













