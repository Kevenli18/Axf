$(function () {
    $(".confirm").click(function () {
        let $confirm = $(this);
    //    查找父级元素
        let cartid = $confirm.parent("div").attr("cartid");
        $.getJSON('/axf/changecarts/', {'cart_id': cartid}, function (data) {
            console.log(data);
            if (data.status == '200'){
                if (data.is_select){
                    $confirm.find("span").find("span").html("√");
                    if (data.all_select){
                        $(".all_select span span").html("√")
                    } else {
                        $(".all_select span span").html("")
                    }
                }
                else {
                    $confirm.find("span").find("span").html("");
                    $(".all_select span span").html("")
                }

                $("#total_price").html(data.total_price)

            }
        })
    });

    $(".all_select").click(function () {
        let select_list = [];
        let un_select_list = [];
        $(".menuList").each(function () {
            let $menuList = $(this);
            let cartid = $menuList.attr("cartid");
            let content = $menuList.find(".confirm span span").html();
            //trim 去掉内容两端的空格
            if (content.trim().length){
                select_list.push(cartid)
            } else {
                un_select_list.push(cartid)
            }
            //有未选中的情况发送给服务器判断
            if (un_select_list.length){
                $.getJSON('/axf/changecartliststatus/', {'action': 'un_select', 'cart_list': un_select_list.join("#")}, function (data) {
                    console.log(data);
                    if (data.status == '200' && data.all_select == true){
                        $(".confirm span span").html("√");
                        $(".all_select span span").html("√")
                        $("#total_price").html(data.total_price)
                    }
                })
            } else{
                $.getJSON('/axf/changecartliststatus/', {'action': 'select', 'cart_list': select_list.join("#")}, function (data) {
                        console.log(data);
                        if (data.status == '200' && data.all_select == false){
                            $(".confirm span span").html("");
                            $(".all_select span span").html("")
                            $("#total_price").html(data.total_price)

                    }
                })
            }
        })
    })
    //添加某个商品数量
    $(".addShopping").click(function () {
        let $add_num = $(this);
        let cart_id = $add_num.parents(".menuList").attr("cartid");
        $.getJSON('/axf/add_cart_good_num/', {'cart_id': cart_id}, function (data) {
            if (data.status == '201'){
                $add_num.prev("span").html(data.new_num);
                $("#total_price").html(data.total_price);
            }
        })
    })
    //减去某个商品数量
    $(".subShopping").click(function () {
        let $sub_num = $(this);
        let cart_id = $sub_num.parents(".menuList").attr("cartid");
        $.getJSON('/axf/sub_cart_good_num/', {'cart_id': cart_id}, function (data) {
            if (data.status == '201'){
                if (data.new_num == 0) {
                    $sub_num.parents(".menuList").remove();
                }else {
                    $sub_num.next("span").html(data.new_num);
                }

                $("#total_price").html(data.total_price);
            }
        })
    })
})



