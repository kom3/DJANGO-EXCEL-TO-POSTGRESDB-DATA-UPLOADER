var uploader ={

    downloadfile: function(){
        console.log("Downloading...")
        $.ajax({
            headers: {
                'X-CSRFToken': $(".token").val()
            },
            type: "POST",
            url: "download",
            data: {}
        }).done(function (data) {
            // if (data == "success") {
            //     window.setTimeout(function(){window.location.reload()}, 1000)
            //     console.log("success")
            // }
            // else {
            //     console.log("fail")
                
            // }
    })
    }
}