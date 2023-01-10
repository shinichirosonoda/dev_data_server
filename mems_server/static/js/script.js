// using global variable
let value1 = "2209-05"
let value2 = "latest";
let value3 = "1"
let start_point = 1;
let stop_point = 100000;
let min_num = 1;
let max_num = 100000;
let sample_name = "";
const start_min = 1;
const stop_max = 100000;

function draw_common(){
    const plotdata = document.getElementById('plotimg');
    const send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point: stop_point, sample_name: sample_name});
    
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

function set_start_stop(){
    $("#text1").val(start_min);
    $("#text2").val(stop_max);
    start_point = start_min;
    stop_point = stop_max;
}


function drawGraph(obj) {
    const idx = obj.selectedIndex;
    value1 = obj.options[idx].value;
    sample_name = "";

    set_sample();
    set_start_stop();
    draw_common();
};

function drawGraph2(obj) {
    const idx = obj.selectedIndex;
    value2 = obj.options[idx].value;

    set_start_stop();
    draw_common();

};

function print_sample(){
    const send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point:stop_point, sample_name: sample_name});
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

function check_start_stop(){
    start_point = check_box("#text1");
    stop_point = check_box("#text2");

    if (start_point > stop_point){
        stop_point = start_point;
        $("#text2").val(stop_point);
    }

    print_sample()
    draw_common();
}

function button(){
    $('#button1').on('click', function(e) {
        e.preventDefault();  // ボタン押下時の動作を抑制
        check_start_stop();
    });
}

function selectSample(obj){
    const idx = obj.selectedIndex;
    value3 = obj.options[idx].value;
    sample_name = value3;

    set_start_stop();
    draw_common();
}

function set_sample(){
    const send_data = JSON.stringify({func: value1, mode: value2, start_point: start_point, stop_point: stop_point, sample_name: sample_name});

    $.ajax({
        method: "POST",
        url: "/list",
        data: send_data,
        contentType: "application/json"
    })
    .done(function(data) {
            $('#selector3').empty();

            for (let i = 0; i < data.sample_list.length; i++){
                $('#selector3').append('<option value='+data.sample_list[i]+'>'+data.sample_list[i]+'</option>');
             }
        }
        
    )
}