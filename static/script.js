
$( document ).ready(function() {

            //file upload example
            var container = $('#indicatorContainerWrap'),
                msgHolder = container.find('.rad-cntnt'),
                containerProg = container.radialIndicator({
                    radius: 100,
                    percentage: true,
                    displayNumber: false
                }).data('radialIndicator');


            container.on({
                'dragenter': function (e) {
                    msgHolder.html("Drop here");
                },
                'dragleave': function (e) {
                    msgHolder.html("Click / Drop file to select.");
                },
                'drop': function (e) {
                    e.preventDefault();
                    handleFileUpload(e.originalEvent.dataTransfer.files);
                }
            });

            $('#prgFileSelector').on('change', function () {
                handleFileUpload(this.files);
            });

            function handleFileUpload(files) {
                msgHolder.hide();
                containerProg.option('displayNumber', true);

                var file = files[0],
                    fd = new FormData();

                fd.append('file', file);


                $.ajax({
                    url: '/upload-file',
                    type: 'POST',
                    data: fd,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        containerProg.option('displayNumber', false);
                        msgHolder.show().html('File upload done.');
                        // console.log(response);
                        setTimeout(function(){window.location.href="/dashboard"},6000);
                    },
                    xhr: function () {
                        var xhr = new window.XMLHttpRequest();
                        //Upload progress
                        xhr.upload.addEventListener("progress", function (e) {
                            
                            if (e.lengthComputable) {
                                var percentComplete = (e.loaded || e.position) * 100 / e.total;
                                containerProg.animate(percentComplete);
                                setTimeout(succupload, 2000);
                                
                            
                            }
                          }, false);
                          function succupload() {
                            let msg = `<span style="color:whitesmoke;">File <u><b>${file.name}</b></u> has been uploaded successfully.</span>`;
                            feedback.innerHTML = msg;
                            document.getElementById("next1").hidden=false;
                            setTimeout(redirect, 3000);
                        }
                        return xhr;
                    }
                });

            }

});
// function next1(){
//     document.getElementById("ques1").hidden=false;
//     document.getElementById("ques2").hidden=true;
//     document.getElementById("upload").hidden=true;
//     document.getElementById("ques3").hidden=true;
    
    
// }
// function next2(){
//     document.getElementById("ques1").hidden=true;
//     document.getElementById("ques2").hidden=false;
//     document.getElementById("upload").hidden=true;
//     document.getElementById("ques3").hidden=true;
    
// }
// function next3(){
//     console.log("next3 is working")
//     document.getElementById("ques1").hidden=true;
//     document.getElementById("ques2").hidden=true;
//     document.getElementById("upload").hidden=true;
//     document.getElementById("ques3").hidden=false;
    
// }

// function back1(){
//     document.getElementById("ques1").hidden=true;
//     document.getElementById("ques2").hidden=true;
//     document.getElementById("upload").hidden=false;
//     document.getElementById("ques3").hidden=true;
    
// }
// function back2(){
//     document.getElementById("ques1").hidden=false;
//     document.getElementById("ques2").hidden=true;
//     document.getElementById("upload").hidden=true;
//     document.getElementById("ques3").hidden=true;
    
// }
// function back3(){
//     document.getElementById("ques1").hidden=true;
//     document.getElementById("ques2").hidden=false;
//     document.getElementById("upload").hidden=true;
//     document.getElementById("ques3").hidden=true;
    
// }
var wrapper = $( "#button-wrapper" );

$( ".submit" ).click(function() {
      if(wrapper.not( ".checked" )) {
            wrapper.addClass( "checked" );
            setTimeout(function(){
                wrapper.removeClass( "checked" );
            }, 8000);
       }
});
