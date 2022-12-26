// global
var value1 = "2209-05"
var value2 = "latest";
var start_point = 1;
var stop_point = 1000;
var max_num = 0;


function draw_common(){
    var plotdata = document.getElementById('plotimg');
    var send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point:stop_point});
    
    $.ajax({
        method: "POST",
        url: "/plot",
        data: send_data,
        contentType: "application/json"
    })
    .done(function(data) {
        plotdata.src = "data:image/png:base64," + data;
    })

    print_sample();
}

function draw_common(){
    var plotdata = document.getElementById('plotimg');
    var send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point:stop_point});
    
    $.ajax({
        method: "POST",
        url: "/plot",
        data: send_data,
        contentType: "application/json"
    })
    .done(function(data) {
        plotdata.src = "data:image/png:base64," + data;
    })
    print_sample(value1);
}

function drawGraph(obj) {
    var idx = obj.selectedIndex;
    value1 = obj.options[idx].value;
    draw_common();
};

function drawGraph2(obj) {
    var idx = obj.selectedIndex;
    value2 = obj.options[idx].value;
    draw_common();

};

function print_sample(){
    var send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point:stop_point});
    $.ajax({
        method: "POST",
        url: "/sample",
        data: send_data,
        contentType: "application/json"
    })
    .done(function(data) {
        
        $("#sample").text(data.sample);
        $("#start_time").text(data.start_time);
        $("#stop_time").text(data.stop_time);
        max_num = data.max_num;
        
        let element1 = document.getElementById("text1");
        let element2 = document.getElementById("text2");

        if (Number(element1.value) < 1){
            element1.value = 1;
        } else if (Number(element1.value) > Number(max_num)){
            element1.value = max_num;
        }
 
        if (Number(element2.value) > Number(max_num)){
            element2.value = max_num;
        } else if (Number(element1.value) > Number(element2.value)){
            element2.value = element1.value;
        }

    });
}

function botton(){
    $(function() {
        $('#button1').click(function(e) {
            e.preventDefault();  // ボタン押下時の動作を抑制

            if (!Number.isNaN(Number($('#text1').val()))){
                start_point = $('#text1').val();
            }
            if (!Number.isNaN(Number($('#text2').val()))){
                stop_point = $('#text2').val();
            }
            
            draw_common();
        });
    });
}