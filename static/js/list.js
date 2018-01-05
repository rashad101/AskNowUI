LIMIT = 3
COUNT = 1

function loadmore(resourcejson) {
    var listImg = []
    $(".list img").each(function () {
        el = $(this);
        var link = el.attr("id");
        listImg.push(link)

    });

    for (var i = 0; i < listImg.length; i++){
        var image_x = document.getElementById(listImg[i]);
        image_x.parentNode.removeChild(image_x);
    }
}



function loadListPage(resourcejson){
    // Javascript function JSON.parse to parse JSON data
    question = resourcejson.question;
    document.getElementsByClassName("showQuestion")[0].innerHTML=question;
    answer = resourcejson.answer;
    abstract = resourcejson.abstract;
    var length = Object.keys(answer).length;
    if (length<LIMIT){
        LIMIT = length
    }
    for (var i=0; i<LIMIT; i++){
        var newitem = "<div class='list-item'>" +
        "          <div class='list-content'>" +
        "            <h2>"+answer[i]+"</h2>" +
        "            <p>"+abstract[i]+"</p>" +
        "            <a>Show detailed</a>" +
        "          </div>" +
        "        </div>"
    $(".list").append(newitem);
    }

   
    $( "#load" ).click(function() {
        for (var i=LIMIT*COUNT; i<LIMIT*(COUNT+1); i++){
            if (i>=length){
                document.getElementById('load').innerHTML= "Loading done"
            }
            else{
                var newitem = "<div class='list-item'>" +
                              "<div class='list-content'>" +
                              "<h2>"+answer[i]+"</h2>" +
                              "<p>"+abstract[i]+"</p>" +
                              "<a>Show detailed</a>" +
                              "</div>" +
                              "</div>"
               $(".list").append(newitem);}             
        }
        COUNT = COUNT +1
    });
}
