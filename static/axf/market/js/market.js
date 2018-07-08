$(function () {
    $("#all_type").click(function () {
        console.log('全部类型');
        $('#all_type_container').show();
        $('#sort_rule_container').hide();
        $(this).find("span").find("span").removeClass("glyphicon-menu-down").addClass("glyphicon-menu-up");
        $('#sort_rule').find("span").find("span").removeClass("glyphicon-menu-up").addClass("glyphicon-menu-down");
    });

    $("#all_type_container").click(function () {
        $(this).hide();
        $("#all_type").find("span").find("span").removeClass("glyphicon-menu-up").addClass("glyphicon-menu-down");
    });

    $('#sort_rule').click(function () {
        console.log('排序类型');
        $("#all_type_container").hide();
        $("#sort_rule_container").show();
        $(this).find("span").find("span").removeClass("glyphicon-menu-down").addClass("glyphicon-menu-up");
        $("#all_type").find("span").find("span").removeClass("glyphicon-menu-up").addClass("glyphicon-menu-down");
    });

    $("#sort_rule_container").click(function () {
         $(this).hide();
        $("#sort_rule").find("span").find("span").removeClass("glyphicon-menu-up").addClass("glyphicon-menu-down");
    });
    
    //添加到购物车
    $(".addShopping").click(function () {
        console.log('添加到购物车');
        var goodsid = $(this).attr("goodsid");
        var $add = $(this);
        //$(this).prop()
        $.getJSON("/axf/add_cart/",{"goodsid": goodsid}, function (data) {
            if (data.status == '902') {
                 window.open('/axf/user_login/', target="_self");
            }else if (data.status == '201'){
                console.log(data);
                $add.prev("span").html(data.c_goods_num)
            }
        })
    })
});
