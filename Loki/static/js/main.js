$(document).ready(function() {
    //id 為 submit 的元素被按下 (click) 時，執行 submit() 這支程式
    $("#submit").click(function(){
        submit();
    });
    var selectMenu = document.getElementById("dropdownList");
    selectMenu.addEventListener("change", function() {
        select();
        submit();
    });
    //定義 select() 的內容如下
    function select(){
        var selectMenu = document.getElementById("dropdownList");
        var selectedOption = selectMenu.value;
        var inputSTR = document.getElementById("inputSTR");
        var inputSTR = selectedOption
        $("#inputSTR").html(inputSTR);
    };
    //定義 submit() 的內容如下
    function submit(){
        //console.log($("#runLLM").is(':checked'));
        $("#thinking").removeClass("d-none");                                //顯示處理動畫
        var payload = {};                                        //準備上傳的內容為 payload
        payload["inputSTR"] = $("#inputSTR").text();              //將輸入區內的字串值載入 payload 中，給定 key 為 "inputSTR"
        payload["runLLM"] = $("#runLLM").is(':checked');
        $("#result").val("");                                   //將 id 為 result 的結果呈現區清空
        //console.log("準備要上傳："+payload["inputSTR"]);
        $.ajax({url: "/gua",                                     //使用 $.ajas() 功能將內容送出
                data: JSON.stringify(payload),
                type: "POST",
                dataType: "json",
                contentType: "application/json;charset=utf-8",
                timeout: 20000,
            success: function(returnData){                       //若成功處理，則將 id 為 result 的區塊填入 returnData 的 checkResult 值。
                console.log(returnData.chatgptResult);
                $("#inputSTR").html(returnData.checkResult);
                $("#ChatGPToutputSTR").html(returnData.chatgptResult);
                $("#thinking").addClass("d-none");                        //隱藏處理動畫
            },
            error: function(xhr, ajaxOptions, thrownError){     //若處理失敗，跳出錯誤原因資訊。
                alert("error: "+ xhr.status);
                alert(thrownError);
            }
        });
    }
});