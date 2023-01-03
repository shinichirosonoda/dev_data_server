// global
let value1 = "2209-05"
let value2 = "latest";
let start_point = 1;
let stop_point = 1000;
let min_num = 1;
let max_num = 0;


function draw_common(){
    const plotdata = document.getElementById('plotimg');
    const send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point:stop_point});
    
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
    const plotdata = document.getElementById('plotimg');
    const send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point:stop_point});
    
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
    const idx = obj.selectedIndex;
    value1 = obj.options[idx].value;
    draw_common();
};

function drawGraph2(obj) {
    const idx = obj.selectedIndex;
    value2 = obj.options[idx].value;
    draw_common();

};

function print_sample(){
    const send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point:stop_point});
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
        
        /*
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
        }*/

        start_point = check_box("#text1");
        stop_point = check_box("#text2");

    });
}

function check_box(box_name){
    let num = parseInt($(box_name).val());
    if(num > max_num){ $(box_name).val(max_num)};
    if(num < min_num){ $(box_name).val(min_num)};
    num = parseInt($(box_name).val());

    return num
}

function botton(){
    $(function() {
        $('#button1').click(function(e) {
            e.preventDefault();  // ボタン押下時の動作を抑制

            start_point = check_box("#text1");
            stop_point = check_box("#text2");

            if (start_point > stop_point){
                stop_point = start_point;
                $("#text2").val(stop_point);
            }

            print_sample()
            draw_common();
        });
    });
}